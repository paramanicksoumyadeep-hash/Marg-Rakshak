import motor.motor_asyncio
import json
import os
from dotenv import load_dotenv

load_dotenv()

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")
with open(CONFIG_PATH, "r") as f:
    config = json.load(f)

MONGO_URI = os.getenv("MONGO_URI", config.get("MONGO_URI", "mongodb://localhost:27017"))
DB_NAME = os.getenv("DB_NAME", config.get("DB_NAME", "drishti_challan_db"))

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]

async def get_db():
    return db
