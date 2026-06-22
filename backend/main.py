from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import uuid
import datetime
from db import get_db
from pipeline.mock import MockPipeline
from rules import calculate_fine
import json

app = FastAPI(title="Project Drishti Command Center")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

pipeline = MockPipeline()

async def process_batch(batch_id: str, file_names: List[str]):
    db = await get_db()
    for fname in file_names:
        # Simulate processing time
        import asyncio
        await asyncio.sleep(1)
        
        # 1. Run detection
        img_id = str(uuid.uuid4())
        results = pipeline.detect(img_id, fname)
        
        # 2. Store event
        event = {
            "batch_id": batch_id,
            "image_id": img_id,
            "original_file": fname,
            "detections": results,
            "processed_at": datetime.datetime.utcnow().isoformat() + "Z"
        }
        await db.events.insert_one(event)
        
        # 3. Generate challans for each violation + plate combination
        plates = results.get("plates", [])
        plate_number = plates[0]["text"] if plates else "UNKNOWN"
        
        for viol in results.get("violations", []):
            # Lookup history for fine escalation
            past_challans_cursor = db.challans.find({"plate_number": plate_number})
            past_challans = await past_challans_cursor.to_list(length=100)
            
            fine_info = calculate_fine(viol["type"], past_challans, event["processed_at"])
            
            challan_id = f"CH-{datetime.datetime.utcnow().year}-{str(uuid.uuid4())[:6].upper()}"
            challan = {
                "challan_id": challan_id,
                "batch_id": batch_id,
                "plate_number": plate_number,
                "violation_type": viol["type"],
                "amount": fine_info["amount"],
                "status": "pending",
                "evidence_image_url": viol.get("evidence_crop_url", f"/evidence/{img_id}.jpg"),
                "camera_id": "unknown",
                "detected_at": event["processed_at"],
                "detection_source": viol.get("source", "model")
            }
            await db.challans.insert_one(challan)
            
        # Update batch progress
        await db.batches.update_one({"batch_id": batch_id}, {"$inc": {"processed_count": 1}})
        
    await db.batches.update_one({"batch_id": batch_id}, {"$set": {"status": "done"}})


@app.post("/api/upload")
async def upload_files(background_tasks: BackgroundTasks, files: List[UploadFile] = File(...)):
    db = await get_db()
    batch_id = f"batch_{str(uuid.uuid4())[:8]}"
    file_names = [f.filename for f in files]
    
    await db.batches.insert_one({
        "batch_id": batch_id,
        "total_count": len(file_names),
        "processed_count": 0,
        "status": "processing",
        "created_at": datetime.datetime.utcnow().isoformat() + "Z"
    })
    
    background_tasks.add_task(process_batch, batch_id, file_names)
    return {"batch_id": batch_id, "message": "Batch queued for processing."}

@app.get("/api/batches/{id}/status")
async def get_batch_status(id: str):
    db = await get_db()
    batch = await db.batches.find_one({"batch_id": id}, {"_id": 0})
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    return batch

@app.get("/api/batches/{id}/results")
async def get_batch_results(id: str):
    db = await get_db()
    cursor = db.challans.find({"batch_id": id}, {"_id": 0})
    challans = await cursor.to_list(length=1000)
    
    grouped = {}
    for c in challans:
        vt = c["violation_type"]
        if vt not in grouped:
            grouped[vt] = {"count": 0, "challans": []}
        grouped[vt]["count"] += 1
        grouped[vt]["challans"].append(c)
        
    return grouped

@app.get("/api/challans")
async def list_challans(type: str = None, status: str = None):
    db = await get_db()
    query = {}
    if type: query["violation_type"] = type
    if status: query["status"] = status
    cursor = db.challans.find(query, {"_id": 0}).sort("detected_at", -1)
    challans = await cursor.to_list(length=100)
    return {"challans": challans}

@app.get("/api/challans/{id}")
async def get_challan(id: str):
    db = await get_db()
    challan = await db.challans.find_one({"challan_id": id}, {"_id": 0})
    if not challan:
        raise HTTPException(status_code=404, detail="Challan not found")
    return challan

@app.get("/api/plates/{number}")
async def get_plate_dossier(number: str):
    db = await get_db()
    vehicle = await db.vehicles.find_one({"plate_number": number}, {"_id": 0})
    if not vehicle:
        return {"plate_number": number, "status": "NOT FOUND IN REGISTRY"}
        
    cursor = db.challans.find({"plate_number": number}, {"_id": 0})
    history = await cursor.to_list(length=100)
    
    total_due = sum(c["amount"] for c in history if c["status"] == "pending")
    
    vehicle["challan_history"] = history
    vehicle["total_outstanding_amount"] = total_due
    return vehicle

@app.post("/api/challans/{id}/send")
async def send_challan(id: str):
    db = await get_db()
    res = await db.challans.update_one({"challan_id": id}, {"$set": {"status": "sent"}})
    if res.modified_count == 0:
        raise HTTPException(status_code=404, detail="Challan not found or already sent")
    
    challan = await db.challans.find_one({"challan_id": id}, {"_id": 0})
    return {
        "challan_id": challan["challan_id"],
        "status": challan["status"],
        "channel": "sms+email (simulated)",
        "amount": challan["amount"]
    }

@app.get("/api/analytics/summary")
async def get_analytics():
    db = await get_db()
    pipeline = [{"$group": {"_id": "$violation_type", "count": {"$sum": 1}}}]
    cursor = db.challans.aggregate(pipeline)
    type_counts = await cursor.to_list(length=100)
    
    formatted_counts = {item["_id"]: item["count"] for item in type_counts}
    
    return {
        "violations_by_type": formatted_counts,
        "daily_trend": [{"date": datetime.date.today().isoformat(), "count": sum(formatted_counts.values())}],
        "top_repeat_plates": [] # Stub
    }

import random
import xml.etree.ElementTree as ET

_camera_cache = None

@app.get("/api/cameras")
async def get_cameras(q: str = None):
    global _camera_cache
    
    cameras = _camera_cache
    if cameras is None or len(cameras) == 0 or "type" not in cameras[0]:
        cameras = []
        kml_file = os.path.join(os.path.dirname(__file__), "..", "datasets", "cctv", "244d7d27-6a5b-441c-b787-23cf02a697ec.kml")
        try:
            tree = ET.parse(kml_file)
            root = tree.getroot()
            ns = {'kml': 'http://www.opengis.net/kml/2.2'}
            placemarks = root.findall('.//kml:Placemark', ns)
            
            for i, pm in enumerate(placemarks):
                coords_tag = pm.find('.//kml:coordinates', ns)
                name_tag = pm.find('kml:name', ns)
                name = None
                if name_tag is not None and name_tag.text:
                    name = name_tag.text.strip()
                else:
                    for data in pm.findall('.//kml:Data', ns):
                        if data.get('name') == 'name':
                            val_tag = data.find('kml:value', ns)
                            if val_tag is not None and val_tag.text:
                                name = val_tag.text.strip()
                            break
                            
                if not name or name.lower() in ["cctv", "camera", "surveillance camera"]:
                    neighborhoods = ["Koramangala", "Indiranagar", "Whitefield", "Jayanagar", "HSR Layout", "Malleswaram", "Marathahalli", "BTM Layout", "Electronic City", "Bellandur", "Rajajinagar", "Hebbal", "Yelahanka", "Banashankari", "Basavanagudi", "JP Nagar", "Ulsoor", "Shivajinagar", "Majestic", "Vidyaranyapura", "Kengeri", "Yeshwanthpur", "Madiwala", "Domlur", "Kammanahalli", "RT Nagar"]
                    streets = ["Main Road", "Junction", "Cross", "Signal", "Ring Road"]
                    name = f"{random.choice(neighborhoods)} {random.choice(streets)} Node {i%100 + 1}"
                    
                if coords_tag is not None and coords_tag.text:
                    coords = coords_tag.text.strip().split(',')
                    if len(coords) >= 2:
                        lng, lat = float(coords[0]), float(coords[1])
                        
                        severity = round(random.uniform(20.0, 95.0), 1)
                        if severity > 70: color = 'bg-primary'
                        elif severity > 50: color = 'bg-orange-500'
                        else: color = 'bg-yellow-500'
                        
                        cameras.append({
                            "id": str(i+1),
                            "name": name,
                            "rank": 0,
                            "severity": severity,
                            "change": round(random.uniform(-10.0, 10.0), 1),
                            "violations": int(severity * random.uniform(1.5, 3.0)),
                            "lat": lat,
                            "lng": lng,
                            "color": color,
                            "type": "active" # Default all to active initially
                        })
        except Exception as e:
            print(f"Error parsing KML: {e}")
            return {"cameras": []}

        # Randomize the list once to pick random active vs hotspots
        random.seed(42)
        random.shuffle(cameras)
        
        # Make the first 200 active cameras, and the next 200 hotspots (no camera)
        for i in range(len(cameras)):
            if i < 200:
                cameras[i]["type"] = "active"
            elif i < 400:
                cameras[i]["type"] = "hotspot"
                cameras[i]["name"] = f"{cameras[i]['name']} (Hotspot)"
                cameras[i]["color"] = "bg-orange-500" # Hotspots are orange
            else:
                cameras[i]["type"] = "inactive" # The rest we won't show unless searched

        # Sort by severity descending to assign rank
        cameras.sort(key=lambda x: x["severity"], reverse=True)
        for idx, c in enumerate(cameras):
            c["rank"] = idx + 1
            
        _camera_cache = cameras

    # Apply search filter
    if q and q.strip():
        query = q.lower().strip()
        filtered_cameras = [c for c in cameras if query in c["name"].lower() and c["type"] in ["active", "hotspot"]]
        return {"cameras": filtered_cameras}
    else:
        # Return 200 active and 200 hotspots
        default_cameras = [c for c in cameras if c["type"] in ["active", "hotspot"]]
        return {"cameras": default_cameras[:400]}

import os
import shutil
from fastapi.staticfiles import StaticFiles

# Serve static files for evidence images
os.makedirs("static/uploads", exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

try:
    from ultralytics import YOLO
    model = YOLO('./best.pt')
except Exception as e:
    print(f"Failed to load YOLO model: {e}")
    model = None

@app.post("/api/predict_images")
async def predict_images(request: Request, images: List[UploadFile] = File(...)):
    if not model:
        raise HTTPException(status_code=500, detail="YOLO model not loaded.")
        
    predictions = []
    base_url = str(request.base_url).rstrip("/")
    
    for img in images:
        file_path = f"static/uploads/{uuid.uuid4()}_{img.filename}"
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(img.file, buffer)
            
        results = model(file_path, conf=0.25)
        
        # Process results
        for r in results:
            boxes = r.boxes
            class_ids = boxes.cls.cpu().numpy()
            
            # Find vehicle types in the image
            vehicle_classes = [0, 1, 2, 3, 4, 5, 22] # car, motorcycle, bus, truck, auto, bicycle, vehicle
            violation_classes = [9, 12, 15, 19, 21] # no_helmet, no_seatbelt, red_light, triple_rider, wrong_side_vehicle
            
            vehicles_found = [model.names[int(c)] for c in class_ids if int(c) in vehicle_classes]
            violations_found = [model.names[int(c)] for c in class_ids if int(c) in violation_classes]
            
            # If no specific vehicle is found but violations are, default to 'Unknown Vehicle'
            primary_vehicle = vehicles_found[0] if vehicles_found else "Unknown Vehicle"
            
            # Check if a license plate is detected (class 10)
            has_plate = any(int(c) == 10 for c in class_ids)
            mock_plate = f"KA-01-{random.choice(['AA', 'MB', 'NX'])}-{random.randint(1000, 9999)}" if has_plate else "Not Visible"
            
            if not violations_found:
                predictions.append({
                    "image_url": f"{base_url}/{file_path}",
                    "image_id": str(uuid.uuid4()),
                    "vehicle_type": primary_vehicle,
                    "vehicle_number": mock_plate,
                    "challan_type": "No Violation",
                    "amount": 0
                })
            else:
                for viol in violations_found:
                    # Calculate fine
                    fine_amount = 500 # Default
                    if viol == 'no_helmet': fine_amount = 500
                    elif viol == 'no_seatbelt': fine_amount = 1000
                    elif viol == 'triple_rider': fine_amount = 1500
                    elif viol == 'wrong_side_vehicle': fine_amount = 2000
                    elif viol == 'red_light': fine_amount = 1000
                    
                    predictions.append({
                        "image_url": f"{base_url}/{file_path}",
                        "image_id": str(uuid.uuid4()),
                        "vehicle_type": primary_vehicle,
                        "vehicle_number": mock_plate,
                        "challan_type": viol,
                        "amount": fine_amount
                    })
                
    return {"predictions": predictions}
