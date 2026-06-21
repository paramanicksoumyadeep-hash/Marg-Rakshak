import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
import json
import os
import random
from datetime import datetime, timedelta

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")
with open(CONFIG_PATH, "r") as f:
    config = json.load(f)

MONGO_URI = config.get("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = config.get("DB_NAME", "drishti_challan_db")

async def seed_db():
    print("Connecting to MongoDB...")
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[DB_NAME]
    
    print("Clearing existing vehicles and challans (for demo)...")
    await db.vehicles.delete_many({})
    await db.challans.delete_many({})
    await db.batches.delete_many({})
    
    print("Seeding synthetic VAHAN vehicle registry...")
    vehicles = []
    
    # We generated plate numbers like KA01AB1000 - KA01AB1099 in the mock pipeline
    for i in range(100):
        plate = f"KA01AB{1000 + i}"
        vehicles.append({
            "plate_number": plate,
            "owner_name": f"Synthetic Owner {i} — Demo Data",
            "vehicle_class": "two_wheeler" if i % 2 == 0 else "four_wheeler",
            "make_model": "Honda Activa" if i % 2 == 0 else "Maruti Swift",
            "registration_date": (datetime.now() - timedelta(days=random.randint(300, 3000))).strftime("%Y-%m-%d"),
            "insurance_status": "valid" if i % 10 != 0 else "expired",
            "puc_status": "valid" if i % 5 != 0 else "expired",
            "is_synthetic": True
        })
        
    await db.vehicles.insert_many(vehicles)
    print(f"Seeded {len(vehicles)} vehicles.")
    
    # Optionally seed some past challan history
    print("Seeding historical challans...")
    past_challans = []
    for i in range(20):
        plate = f"KA01AB{1000 + random.randint(0, 99)}"
        past_challans.append({
            "challan_id": f"CH-HIST-{1000+i}",
            "plate_number": plate,
            "violation_type": "helmet_non_compliance",
            "amount": 1000,
            "status": "paid" if i % 2 == 0 else "pending",
            "evidence_image_url": "/evidence/demo_history.jpg",
            "camera_id": "cam_001_junction_A",
            "detected_at": (datetime.now() - timedelta(days=random.randint(1, 100))).isoformat() + "Z",
            "detection_source": "simulated"
        })
        
    await db.challans.insert_many(past_challans)
    print(f"Seeded {len(past_challans)} historical challans.")
    print("Seeding complete.")

if __name__ == "__main__":
    asyncio.run(seed_db())
