import asyncio
import httpx
import logging
import json
import time
from livekit.agents import JobContext, WorkerOptions, cli, Agent, AgentSession
from livekit.plugins import deepgram, groq, elevenlabs
from app.modules.tools.registry import get_all_tools

# Logging setup (taake terminal mein errors saaf dikhein)
logger = logging.getLogger("voice-agent")
logger.setLevel(logging.INFO)

BACKEND_URL = 'http://localhost:8000'

async def get_session_id(room_name: str) -> str:
    """Backend se session_id fetch karta hai based on room name."""
    async with httpx.AsyncClient() as client:
        try:
            res = await client.get(f"{BACKEND_URL}/api/v1/session/by-room/{room_name}")
            if res.status_code == 200:
                return res.json()["session_id"]
        except Exception as e:
            logger.error(f"Failed to get session_id: {e}")
    return None

async def entrypoint(ctx: JobContext):
    await ctx.connect()

    # 1. Get session ID from DB via Backend API
    session_id = await get_session_id(ctx.room.name)
    if not session_id:
        logger.error("Could not find session ID! Transcripts will not be saved.")

    # 2. Setup Agent Session
    session = AgentSession(
        stt=deepgram.STT(),
        llm=groq.LLM(model='openai/gpt-oss-120b'),
       # tts=elevenlabs.TTS(),
        tts=deepgram.TTS(model='aura-2-andromeda-en'),
        turn_detection='vad',
        min_endpointing_delay=0.1,
    )

    # 3. Define Agent
    agent = Agent(
        instructions="""You are VoxLive, a helpful AI voice assistant. Keep answers short. 
        Before calling a tool, always say a quick filler like 'Let me check that for you...'
        
        CRITICAL RULES FOR PLATFORMS:
        The user might mispronounce 'Daraz' as 'Daraj', 'Rask', 'Daras', 'Tara', or 'Taraz'. 
        NO MATTER what it sounds like, if it's related to orders, ALWAYS assume they mean 'Daraz' or 'Shopify' and pass 'daraz' or 'shopify' to the tool.
        
        RULES FOR TOOLS:
        1. If the user asks for a general summary (e.g., "How many orders?", "Aaj ke orders batao"), use the 'get_real_order_summary' tool.
        2. ONLY use 'check_order_status' if the user provides a specific order ID (like ORD-123).""",
        
        tools=get_all_tools()
    )

    # --- EVENT LISTENERS ---

    # A. Transcripts Save (REQ-VOX-040)
    @session.on("conversation_item_added")
    def on_conversation_item(item):
        if not session_id: return
        role = item.item.role
        text = item.item.text_content
        if text:
            asyncio.create_task(send_utterance(session_id, role, text))

    # B. Tool Logs Save (REQ-VOX-034)
    @session.on("function_tools_executed")
    def on_tools_executed(info):
        if not session_id: return
        for fnc_call in info.function_calls:
            asyncio.create_task(send_tool_log(session_id, fnc_call))

    # C. Interruption Tracking (REQ-VOX-023)
    @session.on('user_interrupted')
    def on_user_interrupted():
        if session_id:
            asyncio.create_task(update_interruption_count(ctx.room.name))

    # 4. Start Session
    await session.start(room=ctx.room, agent=agent)
    
    await session.generate_reply(
        instructions='Say hello and ask how you can help them today.'
    )


# --- HELPER FUNCTIONS TO SEND DATA TO BACKEND ---

async def send_utterance(session_id: str, role: str, text: str):
    """Sends transcribed text to backend to save in DB."""
    payload = {
        "role": role, 
        "text": text, 
        "start_ms": 0, # LiveKit v1.x timings are handled internally, can be enhanced later
        "end_ms": 0
    }
    async with httpx.AsyncClient() as client:
        try:
            await client.post(f"{BACKEND_URL}/api/v1/session/{session_id}/utterance", json=payload)
        except Exception as e:
            logger.error(f"Failed to save utterance: {e}")

async def send_tool_log(session_id: str, info):
    """Sends tool execution details to backend to save in DB."""
    try:
        # 1. Outputs ko ek dictionary mein map karo (call_id -> output)
        output_map = {}
        if hasattr(info, 'function_call_outputs') and info.function_call_outputs:
            for out in info.function_call_outputs:
                output_map[out.call_id] = out.output

        # 2. Har function call ke liye payload banao
        for fnc_call in info.function_calls:
            # Arguments string hoti hain, unhe dict mein convert karo
            args_dict = json.loads(fnc_call.arguments) if isinstance(fnc_call.arguments, str) else fnc_call.arguments
            
            # Output nikalo
            output = output_map.get(fnc_call.call_id, "No output returned")

            payload = {
                "tool_name": fnc_call.name,
                "args": args_dict,
                "result": {"output": str(output)}, # Dict format mein wrap kiya
                "latency_ms": 100, # Abhi ke liye placeholder
                "success": True
            }
            
            async with httpx.AsyncClient() as client:
                await client.post(f"{BACKEND_URL}/api/v1/session/{session_id}/tool-log", json=payload)
                
    except Exception as e:
        logger.error(f"Failed to save tool log: {e}")

async def update_interruption_count(room_name: str):
    """Sends barge-in event to backend."""
    try:
        async with httpx.AsyncClient() as client:
            await client.post(f'{BACKEND_URL}/api/v1/session/interruption', json={'room_name': room_name})
    except Exception as e:
        logger.error(f'Failed to update interruption count: {e}')


if __name__ == '__main__':
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))