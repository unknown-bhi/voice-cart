import asyncio
from app.core.redis import check_and_register_session, remove_session

async def test():
    user = 'test-user-9'
    print("⏳ Testing Redis Sessions...")
    
    print('Session 1 (True aana chahiye):', await check_and_register_session(user))
    print('Session 2 (True aana chahiye):', await check_and_register_session(user))
    print('Session 3 (False aana chahiye):', await check_and_register_session(user))
    
    await remove_session(user)
    
    print('After 1 ends, Session 4 (True aana chahiye):', await check_and_register_session(user))
    
    # Test ke baad data saaf karne ke liye (Optional)
    await remove_session(user)
    await remove_session(user)

if __name__ == "__main__":
    asyncio.run(test())