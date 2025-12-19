import motor.motor_asyncio
from app.config.settings import settings
import certifi

# Get database name from settings
mongo_database = settings.MONGODB_DATABASE


client = motor.motor_asyncio.AsyncIOMotorClient(
    settings.MONGODB_URL,
    tls=True,
    tlsCAFile=certifi.where(),       
    tlsAllowInvalidCertificates=False  
)


database = client[mongo_database]

task_collection = database.get_collection("tasks")

counter_collection = database.get_collection("counters")


async def get_next_task_id():
    """
    Auto-increment task_id using a counters collection.
    """
    result = await counter_collection.find_one_and_update(
        {"_id": "task_id"},
        {"$inc": {"seq": 1}},
        upsert=True,
        return_document=True
    )
    return result["seq"]
