import asyncio
from sqlalchemy import text
from app.core.db import engine

async def test_connection():
    print("⏳ Database se connect karne ki koshish ki ja rahi hai...")
    try:
        # Engine ke zariye database se connect karna
        async with engine.connect() as conn:
            # Ek aasan sa SQL query chalana (SELECT 1)
            await conn.execute(text('SELECT 1'))
            print("✅ Database Connected Successfully!")
            
    except Exception as e:
        print("\n❌ Database se connect nahi ho saka!")
        print(f"Error Detail: {e}")
        print("Yaqeeni banayein ke Docker Desktop open hai aur aapka postgres container 'Up' status mein hai.")
        
    finally:
        # Kaam khatam hone ke baad connection pool ko band karna
        await engine.dispose()

if __name__ == "__main__":
    # Async function ko run karna
    asyncio.run(test_connection())