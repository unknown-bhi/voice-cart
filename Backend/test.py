import redis.asyncio as redis
from app.core.config import settings


redis_client = redis.from_url(settings.REDIS_URL, decode_responses =True)

SESSION_TTL_SECONDS = 15

async def check_and_register_session(user_id :str):

    key =f'user:{user_id}:active_sessions'

    current_count = await redis_client.incr(key)

    if current_count ==1:
        await redis_client.expire(key, SESSION_TTL_SECONDS)

    if current_count > 2:

        await redis_client.decr(key)
        return False
    return True

async def remove_session(user_id : str):
    key =f'user:{user_id}:active_sessions' 
    current_count =await redis_client.decr(key)
    if current_count < 0:
        await redis_client.set(key,0)