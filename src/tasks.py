import os
from celery import Celery

# Import your core functions
from .ai_detection.detect import detect_objects_yolo
from .gis_analysis.analyze import check_encroachments
from .reports.generate_report import generate_pdf_report

# Define the Celery application
celery_app = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

@celery_app.task
def process_image_for_encroachment(image_path, drone_telemetry):
    """
    Celery task to run the AI and GIS analysis in the background.
    """
    # Step 1: Object Detection
    detected_structures = detect_objects_yolo(image_path, drone_telemetry=drone_telemetry)
    
    # Step 2: Geospatial Analysis
    road_path = "data/gis_boundaries/roads.shp"
    encroachments = check_encroachments(detected_structures)
    
    # Step 3: Generate the report
    generate_pdf_report(encroachments, image_path)
    
    # Clean up the temporary image
    os.remove(image_path)
    
    return {"status": "completed", "encroachments": encroachments}