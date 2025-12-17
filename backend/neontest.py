# import os
# import asyncpg
# import asyncio
# from dotenv import load_dotenv

# load_dotenv()  # Load .env

# DATABASE_URL = os.getenv("NEON_DATABASE_URL")

# async def test_connection():
#     try:
#         conn = await asyncpg.connect(DATABASE_URL)
#         row = await conn.fetchrow("SELECT NOW() AS current_time")
#         print("✅ Connected to Neon! Current time:", row["current_time"])
#         await conn.close()
#     except Exception as e:
#         print("❌ Failed to connect:", e)

# asyncio.run(test_connection())

import socket

host = "56707107-2e68-459d-a7e9-3733be6a8a17.europe-west3-0.gcp.cloud.qdrant.io"
print(socket.gethostbyname(host))
