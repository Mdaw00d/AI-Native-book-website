# db.py
import os
import asyncpg
import asyncio
from dotenv import load_dotenv

load_dotenv()
DATABASE_URL = os.getenv("NEON_DATABASE_URL")

async def save_chunk_metadata(url, text_length):
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        await conn.execute(
            "INSERT INTO chunks_metadata(url, text_length) VALUES($1, $2)",
            url, text_length
        )
    finally:
        await conn.close()

def save_metadata_sync(url, text_length):
    asyncio.run(save_chunk_metadata(url, text_length))
