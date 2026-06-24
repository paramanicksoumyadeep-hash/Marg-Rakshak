# 🚦 Marg-Rakshak — Project Drishti Command Center

**Automated Traffic Violation Detection & E-Challan Command Center**

Marg-Rakshak ("Guardian of the Road") is a full-stack system for turning raw traffic camera footage into enforceable e-Challans. It ingests CCTV evidence, runs it through a pluggable computer vision pipeline to detect violations, matches license plates against a VAHAN-style vehicle registry, and generates config-driven fines — with full traceability from detection to dispatch.

[![Python](https://img.shields.io/badge/Python-58.4%25-3776AB?logo=python&logoColor=white)](https://github.com/paramanicksoumyadeep-hash/Marg-Rakshak)
[![TypeScript](https://img.shields.io/badge/TypeScript-38.6%25-3178C6?logo=typescript&logoColor=white)](https://github.com/paramanicksoumyadeep-hash/Marg-Rakshak)
[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![React](https://img.shields.io/badge/Frontend-React%20%2B%20Vite-61DAFB?logo=react&logoColor=black)](https://vitejs.dev/)
[![MongoDB](https://img.shields.io/badge/Database-MongoDB%20Atlas-47A248?logo=mongodb&logoColor=white)](https://www.mongodb.com/atlas)
[![Docker](https://img.shields.io/badge/Deploy-Docker%20Compose-2496ED?logo=docker&logoColor=white)](https://docs.docker.com/compose/)

---

## 📖 Overview

Most "AI traffic enforcement" demos hide behind a black box — you see a violation flagged, but never *why*. Marg-Rakshak is built around a **transparency mandate**: every single violation traced back to the platform must show exactly which detection tier produced it, so the result is defensible, auditable, and judge-ready rather than a guess dressed up as AI.

The system is designed to be developed and demoed end-to-end **without requiring a GPU or a trained model**, while still leaving a clean path to plug in real production-grade detection later.

---

## 🏗️ Architecture

| Layer | Technology |
|---|---|
| **Frontend** | Vite + React + TypeScript + Tailwind CSS *(TomTom Command Center theme)* |
| **Backend** | FastAPI (Python) |
| **Database** | MongoDB Atlas (simulated locally via Docker) |
| **CV Pipeline** | Pluggable 3-tier Computer Vision Engine |
| **Orchestration** | Docker Compose |

### Repository layout

```
Marg-Rakshak/
├── backend/          # FastAPI service, pipeline adapters, seed scripts
├── frontend/         # Vite + React + TS command center UI
├── dashboard/         # Command-center dashboard views
├── ui/                # Shared UI components
├── detection/         # Violation detection logic
├── ocr/               # License plate OCR
├── preprocessing/      # Frame/image preprocessing utilities
├── violations/         # Violation rules / records
├── evidence/           # Captured evidence storage
├── data/, datasets/cctv/  # Sample & training data
├── eval/               # Model/pipeline evaluation
├── configs/             # Fine schedules & pipeline configuration
├── test_images/         # Sample frames for quick testing
├── docker-compose.yml
├── main.py
├── train.py
├── prepare_data.py / prepare_data_linux.py
├── convert_idd.py
└── requirements.txt
```

---

## 🧠 The 3-Tier Detection Pipeline

Every violation is stamped with the tier that produced it, so nothing pretends to be more accurate than it is:

| Tier | What it actually does |
|---|---|
| 🧪 **Mock** *(active by default)* | Deterministic synthetic detections that match the real JSON contract exactly — lets you build and demo the entire UI/flow instantly, no GPU required. |
| ⚙️ **Lite** | Genuine pretrained object detection (COCO YOLO) combined with spatial heuristic rules — real detection, lightweight model. |
| 🎯 **Real** | Your own trained YOLO model, wired in through an adapter stub (`backend/pipeline/real.py`) — drop in your weights when ready. |

> ⚠️ **Disclaimer on fines:** Fine amounts in this demo are pulled from `backend/config.json`. State governments periodically revise these figures under the Motor Vehicles (Amendment) Act, 2019. Always verify current official rates at **[parivahan.gov.in](https://parivahan.gov.in)** before any real-world dispatch — this system is a command center, not a legal authority.

---

## 🚀 Quick Start

### 1. Start the environment

```bash
docker-compose up
```

### 2. Seed the synthetic registry

Populate MongoDB with a synthetic VAHAN-style vehicle registry and historical challan records:

```bash
cd backend
pip install -r requirements.txt
python seed.py
```

### 3. Access the Command Center

| Service | URL |
|---|---|
| 🖥️ App | [https://marg-rakshak-ai.vercel.app/](https://marg-rakshak-ai.vercel.app/) |

---

## 🧰 Tech Stack

- **Languages:** Python (58.4%) · TypeScript (38.6%) · CSS (1.9%)
- **Computer Vision:** YOLO (COCO-pretrained + custom-trainable adapter)
- **OCR:** License plate recognition module
- **API:** FastAPI with auto-generated OpenAPI docs
- **Frontend:** React + Vite + Tailwind CSS, styled as a real-time command center

---

## 🗺️ Roadmap Ideas

- [ ] Wire up the `Real` tier with a production-trained YOLO model
- [ ] Live CCTV stream ingestion (RTSP) instead of static frame batches
- [ ] Automated e-Challan dispatch integration
- [ ] Role-based access for traffic authority dashboards
- [ ] Multi-state fine-schedule configs beyond `config.json`

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome. If you're extending the detection pipeline, please keep new tiers consistent with the existing JSON contract so the transparency mandate holds for every result the system produces.

## 📄 License

No license file is currently published in this repository. Until one is added, please contact the repository owner before reusing this code.

---

<p align="center"><i>Built to make traffic enforcement explainable — not just automated.</i></p>
