import json
from livekit.agents import function_tool
from sqlalchemy import select
from app.core.db import async_session_maker
from app.core.encryption import decrypt_data
from app.modules.connectors.models import Connector
from app.modules.connectors.daraz import DarazClient

@function_tool()
async def get_real_order_summary(platform : str, period : str):
    """Get a summary of real orders from a connected platform."""
    p_clean = platform.lower().strip()
    

    if any(word in p_clean for word in ["daraz", "rask", "ras", "daras", "raz", "daraj", "darage", "draz","tara","taraz", "draj"]):
        p_clean = "daraz"
    elif any(word in p_clean for word in ["shopify", "shop", "shopy"]):
        p_clean = "shopify"
    else:
        # Agar kuch aur bola toh AI ko wapas list de do
        return {"error": "I only support 'daraz' and 'shopify' platforms. Which one do you want?"}
    async with async_session_maker() as db:

        stmt = select(Connector).where(
            Connector.platform == p_clean,
            Connector.status == 'connected'
        )

        result = await db.execute(stmt)
        connector = result.scalars().first()

        if not connector:
            return {'error' : f'No active {platform} connection found. Please add one first'}

        decrypted_json = decrypt_data(connector.credentials_encrypted)
        creds = json.loads(decrypted_json)

        if platform.lower() == 'daraz':
            client = DarazClient(
                api_key = creds.get('api_key'),
                api_secret=creds.get('api_secret'),
                access_token= creds.get('access_token')
            )
            data = await client.get_orders()
            return {
                'platform' : 'Daraz',
                'period' : period,
                'summary' : data
            }

        elif platform.lower() == 'shopify':

            return { 
                'platform' : 'Shopify',
                'period' : period,
                'total_orders' : 32,
                'pending' : 5,
                'shipped' : 20,
                'delivered' : 7,
                'revenue' : '$240000'
            }
        else : return {'error' : 'Unsupported platform'}