# Project Drishti Command Center

Automated Traffic Violation Detection & E-Challan Command Center. 
This repository contains a full-stack system for ingesting traffic camera evidence, detecting violations using a pluggable CV pipeline, matching vehicle plates against a VAHAN-style registry, and generating config-driven e-Challans.

## Architecture

- **Frontend**: Vite + React + TypeScript + Tailwind CSS (TomTom Command Center Theme)
- **Backend**: FastAPI (Python)
- **Database**: MongoDB Atlas (simulated locally)
- **Pipeline**: Pluggable 3-Tier Computer Vision Engine

### Pipeline Tiers & Transparency Mandate

Every violation result on this platform traces back to a specific detection source to ensure judge-defensible accountability:
1. **Real**: Your actual trained YOLO model (adapter stubbed in `backend/pipeline/real.py`).
2. **Lite**: Genuine pretrained object detection (COCO YOLO) combined with spatial heuristic rules.
3. **Mock** *(Active by Default)*: Deterministic synthetic detections that match the JSON contract perfectly, allowing you to develop the UI and demo the flow instantly without a GPU.

> **Disclaimer on Fines**: Fines in this demo system are derived from `backend/config.json`. State governments frequently adjust these figures based on the MV(A)A 2019. Always verify official rates on `parivahan.gov.in` before any real-world dispatch.

## Quick Start

### 1. Start the Environment
```bash
docker-compose up
```

### 2. Seed the Synthetic Registry
To populate the MongoDB with the synthetic VAHAN vehicle registry and historical challans:
```bash
cd backend
pip install -r requirements.txt
python seed.py
```

### 3. Access the Command Center
- **Frontend App**: http://localhost:5173
- **Backend API Docs**: http://localhost:8000/docs
