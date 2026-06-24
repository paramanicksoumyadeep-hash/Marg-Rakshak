from fastapi import FastAPI, UploadFile, File, BackgroundTasks, HTTPException, Request, Depends, Response
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional
import uuid
import datetime
import os
import shutil
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

from db import get_db
from pipeline.mock import MockPipeline
from rules import calculate_fine
import json

# SlowAPI setup
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

app = FastAPI(title="Project Drishti Command Center")

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
if not JWT_SECRET_KEY:
    raise RuntimeError("JWT_SECRET_KEY environment variable is required. Please set it in your .env file.")

ALLOWED_ORIGINS = [origin.strip() for origin in os.getenv("ALLOWED_ORIGINS", "http://localhost:5173").split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_origin_regex=r"https://.*\.vercel\.app.*",
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Authorization", "Content-Type"],
)

pipeline = MockPipeline()

# Auth setup
from pydantic import BaseModel, Field
from passlib.context import CryptContext
from jose import JWTError, jwt

SECRET_KEY = JWT_SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserCreate(BaseModel):
    first_name: str
    last_name: str
    username: str
    email: str
    password: str = Field(..., min_length=8)

class UserLogin(BaseModel):
    username: str
    password: str

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[datetime.timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.datetime.utcnow() + expires_delta
    else:
        expire = datetime.datetime.utcnow() + datetime.timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")
        
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")

@app.post("/api/auth/register")
async def register(request: Request, user: UserCreate, response: Response):
    db = await get_db()
    
    # Check if username or email exists
    existing_user = await db.users.find_one({"$or": [{"username": user.username}, {"email": user.email}]})
    if existing_user:
        raise HTTPException(status_code=400, detail="Username or Email already registered")
        
    user_dict = user.model_dump()
    user_dict["hashed_password"] = get_password_hash(user_dict.pop("password"))
    user_dict["created_at"] = datetime.datetime.utcnow()
    
    await db.users.insert_one(user_dict)
    
    # Generate token
    access_token_expires = datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "name": f"{user.first_name} {user.last_name}"}, expires_delta=access_token_expires
    )
    
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    return {"message": "Successfully registered"}

@app.post("/api/auth/login")
async def login(request: Request, user_credentials: UserLogin, response: Response):
    db = await get_db()
    user = await db.users.find_one({"username": user_credentials.username})
    
    if not user or not verify_password(user_credentials.password, user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Invalid username or password")
        
    access_token_expires = datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"], "name": f"{user['first_name']} {user['last_name']}"}, expires_delta=access_token_expires
    )
    
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    return {"message": "Successfully logged in"}

@app.post("/api/auth/demo")
@limiter.limit("5/minute")
async def login_demo(request: Request, response: Response):
    access_token_expires = datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": "demo_surveyor", "name": "Demo Surveyor"}, expires_delta=access_token_expires
    )
    
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        secure=True,
        samesite="none",
        max_age=ACCESS_TOKEN_EXPIRE_MINUTES * 60
    )
    return {"message": "Successfully logged in as demo surveyor"}

@app.get("/api/auth/me")
async def get_me(user = Depends(get_current_user)):
    return {"username": user.get("sub"), "name": user.get("name")}

@app.post("/api/auth/logout")
async def logout(response: Response):
    response.delete_cookie("access_token", httponly=True, secure=True, samesite="lax")
    return {"message": "Logged out"}


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


ALLOWED_MIME = {"image/jpeg", "image/png", "image/webp"}
MAX_FILE_SIZE = 10 * 1024 * 1024 # 10 MB

@app.post("/api/upload")
async def upload_files(background_tasks: BackgroundTasks, files: List[UploadFile] = File(...), user = Depends(get_current_user)):
    db = await get_db()
    batch_id = f"batch_{str(uuid.uuid4())[:8]}"
    
    file_names = []
    for img in files:
        content = await img.read()
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail=f"File {img.filename} is too large")
        if img.content_type not in ALLOWED_MIME:
            raise HTTPException(status_code=415, detail=f"File type {img.content_type} not allowed")
            
        safe_name = f"{uuid.uuid4()}.jpg"
        file_path = Path("static/uploads") / safe_name
        file_path.write_bytes(content)
        file_names.append(safe_name)
    
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
async def get_batch_status(id: str, user = Depends(get_current_user)):
    db = await get_db()
    batch = await db.batches.find_one({"batch_id": id}, {"_id": 0})
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    return batch

@app.get("/api/batches/{id}/results")
async def get_batch_results(id: str, user = Depends(get_current_user)):
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
async def list_challans(type: str = None, status: str = None, user = Depends(get_current_user)):
    db = await get_db()
    query = {}
    if type: query["violation_type"] = type
    if status: query["status"] = status
    cursor = db.challans.find(query, {"_id": 0}).sort("detected_at", -1)
    challans = await cursor.to_list(length=100)
    return {"challans": challans}

@app.get("/api/challans/{id}")
async def get_challan(id: str, user = Depends(get_current_user)):
    db = await get_db()
    challan = await db.challans.find_one({"challan_id": id}, {"_id": 0})
    if not challan:
        raise HTTPException(status_code=404, detail="Challan not found")
    return challan

@app.get("/api/plates/{number}")
async def get_plate_dossier(number: str, user = Depends(get_current_user)):
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
async def send_challan(id: str, user = Depends(get_current_user)):
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
async def get_analytics(user = Depends(get_current_user)):
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
async def get_cameras(q: str = None, user = Depends(get_current_user)):
    global _camera_cache
    
    cameras = _camera_cache
    if not cameras:
        import json
        try:
            with open("real_cameras.json", "r") as f:
                cameras = json.load(f)
        except Exception:
            cameras = config.get("cameras", [])
        _camera_cache = cameras
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
@limiter.limit("10/minute")
async def predict_images(request: Request, images: List[UploadFile] = File(...), user = Depends(get_current_user)):
    if not model:
        raise HTTPException(status_code=500, detail="YOLO model not loaded.")
        
    predictions = []
    base_url = str(request.base_url).rstrip("/")
    
    for img in images:
        content = await img.read()
        if len(content) > MAX_FILE_SIZE:
            raise HTTPException(status_code=413, detail=f"File {img.filename} is too large")
        if img.content_type not in ALLOWED_MIME:
            raise HTTPException(status_code=415, detail=f"File type {img.content_type} not allowed")
            
        safe_name = f"{uuid.uuid4()}.jpg"
        file_path = Path("static/uploads") / safe_name
        file_path.write_bytes(content)
            
        results = model(str(file_path), conf=0.25)
        
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
