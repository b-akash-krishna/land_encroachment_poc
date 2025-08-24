import uvicorn
from fastapi import FastAPI, UploadFile, File
import os
import shutil
import json

# Import functions from other modules
# These are now absolute imports relative to the project root
from src.ai_detection.detect import detect_objects_yolo
from src.gis_analysis.analyze import check_encroachments
from src.reports.generate_report import generate_pdf_report

app = FastAPI()

# Configuration - Correct paths relative to the project root
TEMP_UPLOAD_DIR = "temp_uploads"
ROAD_SHAPEFILE_PATH = "data/gis_boundaries/roads.shp"

@app.on_event("startup")
async def startup_event():
    """Create a temporary directory for file uploads."""
    os.makedirs(TEMP_UPLOAD_DIR, exist_ok=True)

@app.post("/analyze_image/")
async def analyze_image(file: UploadFile = File(...)):
    """
    Main API endpoint to analyze an uploaded image.
    
    Processes the image, runs object detection, performs GIS analysis,
    and returns a JSON of encroachments.
    """
    try:
        # Save the uploaded file temporarily
        file_path = os.path.join(TEMP_UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Step 1: Object Detection
        detected_structures = detect_objects_yolo(file_path)
        
        # Step 2: Geospatial Analysis
        if not os.path.exists(ROAD_SHAPEFILE_PATH):
            return {"error": "Road shapefile not found. Please add to `data/gis_boundaries`."}

        encroachments = check_encroachments(detected_structures, ROAD_SHAPEFILE_PATH)
        
        # Cleanup temporary file
        os.remove(file_path)
        
        return {"status": "success", "encroachments": encroachments}
        
    except Exception as e:
        return {"status": "error", "message": str(e)}

@app.get("/generate_report/")
async def create_report(encroachments_json: str):
    """
    Generates a PDF report from a JSON string of encroachment data.
    """
    try:
        encroachments = json.loads(encroachments_json)
        # The output path for the report is now correct relative to the project root
        report_path = generate_pdf_report(encroachments, output_path=f"reports/encroachment_report.pdf")
        
        return {"report_url": "http://localhost:8000/reports/encroachment_report.pdf"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)