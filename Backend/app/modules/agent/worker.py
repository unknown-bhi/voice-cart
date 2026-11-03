import logging
from livekit.agents import JobContext, WorkerOptions,cli,Agent, AgentSession
from livekit.plugins import deepgram, groq, elevenlabs

logger =logging.getLogger('voice-agent')
logger.setLevel(logging.INFO)

async def entrypoint(ctx: JobContext):

    logger.info(f'Connecting to room{ctx.room.name}')

    await ctx.connect()

    session =AgentSession(
        stt= deepgram.STT(),
        llm= groq.LLM(model='openai/gpt-oss-120b'),
        tts= elevenlabs.TTS()
    )

    agent = Agent(
        instructions ='You are VoxLive, a helpful and friendly AI voice assistant. Keep your answers short and conversational, as this is a voice interface'
    )

    await session.start(
        room=ctx.room,
        agent=agent
    )

    await session.generate_reply(
        instructions= 'Say hello and ask how you can help them today.'
    )

if __name__ == '__main__':

    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))