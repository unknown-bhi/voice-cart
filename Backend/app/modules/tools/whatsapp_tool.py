import httpx
import json
import os
from pathlib import Path
from livekit.agents import function_tool
import logging

logger = logging.getLogger("voice-agent")

CONTACTS_FILE = Path(__file__).parent / "contacts.json"

def get_phone_number(contact_input: str) -> str | None:
    clean_input = contact_input.replace(" ", "").replace("-", "")
    if clean_input.isdigit():
        return clean_input

    try:
        # Check karo file majood hai ya nahi
        if not CONTACTS_FILE.exists():
            logger.error(f"❌ Contacts file NOT FOUND at {CONTACTS_FILE}")
            return None
            
        with open(CONTACTS_FILE, "r", encoding="utf-8") as f:
            contacts = json.load(f)
        
        name_key = contact_input.lower().strip()
        logger.info(f"🔍 Looking for '{name_key}' in contacts: {contacts.keys()}")
        
        return contacts.get(name_key)
    except Exception as e:
        logger.error(f"❌ Error reading contacts: {e}")
        return None

@function_tool()
async def send_whatsapp_message(phone_number_or_name: str, message: str) -> dict:
    """Send a real WhatsApp message to a specific contact. 
    DO NOT ask the user for a phone number if they provide a name. Just pass the name.
    
    Args:
        phone_number_or_name: The name of the contact (e.g., "Ali") OR a phone number.
        message: The text message to send.
    """
    phone_number = get_phone_number(phone_number_or_name)
    
    if not phone_number:
        return {
            "status": "error", 
            "message": f"I don't have a phone number for '{phone_number_or_name}'. Please say the phone number with country code."
        }

    chat_id = f"{phone_number}@c.us"

    url = "http://localhost:2785/api/sendText" 
    
    headers = {
        "Content-Type": "application/json",
        "X-Api-Key": "owa_k1_d21656b3673b2a1fc5771131047b11c661ea3119d776eb852cb21883faa97eed"
    }
    
    payload = {
        "sessionId": "voxlive",
        "chatId": chat_id,
        "text": message
    }

    logger.info(f"📱 Sending WhatsApp to {phone_number_or_name} ({phone_number})...")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(url, json=payload, headers=headers, timeout=10.0)
            
            if response.status_code in [200, 201]:
                logger.info(f"✅ Message sent to {phone_number_or_name}!")
                return {"status": "success", "message": f"Message successfully sent to {phone_number_or_name}."}
            else:
                logger.error(f"❌ Failed: {response.text}")
                return {"status": "error", "message": f"Failed to send: {response.text}"}
                
    except Exception as e:
        logger.error(f"❌ Connection error: {str(e)}")
        return {"status": "error", "message": f"Connection failed: {str(e)}"}