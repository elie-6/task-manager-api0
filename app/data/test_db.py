import asyncio
from app.data.database import client

async def main():
    try:
        # List all databases in your MongoDB cluster
        dbs = await client.list_database_names()
        print("Databases:", dbs)
    except Exception as e:
        print("Error connecting to MongoDB:", e)

asyncio.run(main())
