import asyncio
from app.core.db import engine, Base
# Yahan apne saare models import karna zaroori hai taake Base ko pata chale kaunsi tables banani hain
from app.modules.sessions.models import Session 

async def create_tables():
    print("⏳ Tables create ki ja rahi hain...")
    async with engine.begin() as conn:
        # Yeh line database mein saari tables bana degi
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Tables created successfully!")
    await engine.dispose()

if __name__ == "__main__":
    asyncio.run(create_tables())