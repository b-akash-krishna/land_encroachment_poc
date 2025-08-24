PoC MVP: AI-Powered Drone Surveillance for Land Encroachment Detection
📌 Overview

This repository contains a Proof-of-Concept (PoC) Minimum Viable Product (MVP) for detecting land encroachments on public roads using drone-based aerial imagery combined with AI-powered object detection and geospatial analysis.

The system demonstrates how drones, computer vision, and GIS tools can be integrated to automatically flag unauthorized occupation of government-owned land. While this MVP runs on sample datasets and simulated inputs, it provides a modular foundation for real-world deployment.

🏗 System Architecture

The project is divided into three main modules:

1. Data Processing Pipeline

Input: Aerial images (sample drone video frames or datasets).

AI Object Detection: Pre-trained/fine-tuned YOLOv8 for detecting structures (e.g., buildings, fences, vehicles).

Output: Bounding box coordinates of detected objects.

2. Backend & Geospatial Analysis

Geospatial Data Handling: Uses GeoPandas to load shapefiles or OSM data.

Overlay & Analysis: Compares detected objects with legal land boundaries.

Encroachment Flagging: Identifies and reports structures overlapping with public land buffers.

API: FastAPI backend to process inputs and serve results.

3. Frontend & Reporting

Dashboard: Web-based map visualization with Folium/Leaflet.

Reporting: Generates structured PDF/JSON reports of flagged encroachments.

📂 Project Structure
land_encroachment_poc/
├── data/
│   ├── aerial_images/      # Sample drone frames or video input
│   ├── gis_boundaries/     # Shapefiles (roads, land parcels)
│   └── simulated_data/     # Scripts for generating sample drone input
├── models/
│   ├── yolov8n.pt          # Pre-trained YOLOv8 model
│   └── custom_model.pt     # Fine-tuned weights (optional)
├── src/
│   ├── ai_detection/       # Object detection logic
│   ├── gis_analysis/       # Geospatial overlay logic
│   ├── backend/            # FastAPI service
│   └── reports/            # PDF/JSON reporting
├── frontend/               # Simple Leaflet/Folium dashboard
├── requirements.txt        # Python dependencies
├── run.sh                  # Startup script
└── README.md

📊 Sample Datasets & Simulation

Aerial Images: Use datasets like Stanford Drone Dataset
 or VisDrone2019
.

Property Boundaries: Download from OpenStreetMap or create dummy shapefiles with QGIS.

Drone Simulation: Use a Python script with OpenCV to convert video into sequential frames (simulate_input.py).

⚙️ Tech Stack

AI/Detection: Ultralytics YOLOv8

Geospatial Analysis: GeoPandas, Shapely, OSMnx

Backend: FastAPI + Uvicorn

Visualization: Folium (Leaflet.js)

Reporting: ReportLab

🚀 How to Run

Install dependencies:

pip install -r requirements.txt


Prepare sample data:

Place a video in data/aerial_images/ and run the simulation script.

Add a roads.shp shapefile under data/gis_boundaries/.

Run drone simulation:

python data/simulated_data/simulate_input.py


Start backend service:

uvicorn src.backend.main:app --reload


Open dashboard:
Open frontend/index.html in a browser to view flagged encroachments on a map.

📌 Current Status

✅ Proof-of-Concept pipeline implemented with sample datasets.

✅ AI detection + GIS overlay integration.

✅ Visualization and reporting modules working.

🚧 Next step: Integrate real drone live feed + georeferencing.

🔮 Future Enhancements

Real-time edge AI deployment on drones.

Automated georeferencing between imagery & GIS maps.

Scalable multi-drone coordination.

Automated compliance reporting for municipal authorities.

🌍 Impact

This project demonstrates how AI + GIS + Drones can modernize land governance, urban planning, and smart city management by automating the detection of illegal encroachments.
