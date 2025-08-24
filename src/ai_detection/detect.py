from ultralytics import YOLO
import cv2
from pyproj import Transformer
from shapely.geometry import box

def pixel_to_geographic(bbox, drone_telemetry, image_size=(640, 640)):
    """
    Simulates converting a pixel bounding box to geographic coordinates (lon, lat).
    
    Args:
        bbox (list): Bounding box in pixel coordinates [x1, y1, x2, y2].
        drone_telemetry (dict): Contains drone's location and orientation.
        image_size (tuple): The width and height of the image.
        
    Returns:
        tuple: A tuple of (min_lon, min_lat, max_lon, max_lat)
    """
    # For a PoC, we will simulate the transformation.
    # In a real system, you'd use camera parameters and a robust georeferencing model.
    
    # Get a simple transformation from pixel to geographic space
    # The scale factor is a simplification for a given altitude.
    pixel_scale_x = drone_telemetry['altitude'] / image_size[0]
    pixel_scale_y = drone_telemetry['altitude'] / image_size[1]
    
    x1, y1, x2, y2 = bbox
    center_lon, center_lat = drone_telemetry['location']
    
    # Simple mapping of pixel coordinates to a projected CRS (meters)
    proj_x1 = (x1 - image_size[0]/2) * pixel_scale_x
    proj_y1 = (y1 - image_size[1]/2) * pixel_scale_y
    proj_x2 = (x2 - image_size[0]/2) * pixel_scale_x
    proj_y2 = (y2 - image_size[1]/2) * pixel_scale_y
    
    # Transform from the projected CRS (e.g., UTM) to WGS84 (lat/lon)
    # We use a dummy transformer to demonstrate the concept.
    transformer = Transformer.from_crs("EPSG:3857", "EPSG:4326")
    lon1, lat1 = transformer.transform(proj_x1, proj_y1)
    lon2, lat2 = transformer.transform(proj_x2, proj_y2)
    
    # Note: The above transformation is a simplification. A real implementation would be more complex.
    
    return (lon1, lat1, lon2, lat2)

def detect_objects_yolo(image_path, model_path='models/yolov8n.pt', drone_telemetry=None):
    """
    Uses YOLOv8 to detect objects and return bounding boxes.

    Args:
        image_path (str): Path to the input image.
        model_path (str): Path to the YOLOv8 model weights.

    Returns:
        list: A list of dictionaries, each containing 'class_name', 'bbox' and optionally 'geographic_bbox'.
    """
    # Load a pre-trained YOLOv8n model
    model = YOLO(model_path)
    
    # Run inference on the image
    results = model(image_path)
    
    detections = []
    # Relevant classes: The class names can be mapped from your model.
    # We will generalize to 'structures' for this PoC.
    relevant_classes = [0, 1, 2, 3, 5, 6, 7, 15] # Example classes from COCO dataset
    
    for r in results:
        for box in r.boxes:
            class_id = int(box.cls[0])
            # Filter for a few common structure types as an example
            # In a real-world scenario, you would train a model on specific classes.
            if class_id in relevant_classes:
                # Get bounding box coordinates
                x1, y1, x2, y2 = box.xyxy[0].tolist()
                
                # If telemetry data is available, convert bbox to geographic coords
                if drone_telemetry:
                    lon1, lat1, lon2, lat2 = pixel_to_geographic([x1, y1, x2, y2], drone_telemetry)
                    detections.append({
                        "class_name": model.names[class_id],
                        "bbox": [x1, y1, x2, y2],
                        "geographic_bbox": [lon1, lat1, lon2, lat2]
                    })
                else:
                    detections.append({
                        "class_name": model.names[class_id],
                        "bbox": [x1, y1, x2, y2]
                    })

    return detections

if __name__ == "__main__":
    # Example usage
    # You will need to place a sample image in 'data/aerial_images/'
    # Or, run the simulation script first to generate one.
    sample_image = "../../data/aerial_images/frame_0.jpg"
    
    # Check if the sample image exists before running
    import os
    if not os.path.exists(sample_image):
        print("Sample image not found. Please place 'frame_0.jpg' in 'data/aerial_images/' or run the simulation script.")
    else:
        # Example dummy drone telemetry data
        dummy_telemetry = {
            "location": (-74.006, 40.7128),
            "altitude": 100, # meters
            "orientation": 0 # degrees
        }
        detected_structures = detect_objects_yolo(sample_image, drone_telemetry=dummy_telemetry)
        print(f"Detected structures: {detected_structures}")
        
        # Optional: Draw bounding boxes on the image for visualization
        img = cv2.imread(sample_image)
        for det in detected_structures:
            bbox = det['bbox']
            x1, y1, x2, y2 = map(int, bbox)
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(img, det['class_name'], (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        cv2.imshow("Detected Objects", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()