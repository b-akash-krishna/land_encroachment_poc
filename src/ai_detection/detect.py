from ultralytics import YOLO
import cv2

def detect_objects_yolo(image_path, model_path='models/yolov8n.pt'):
    """
    Uses YOLOv8 to detect objects and return bounding boxes.

    Args:
        image_path (str): Path to the input image.
        model_path (str): Path to the YOLOv8 model weights.

    Returns:
        list: A list of dictionaries, each containing 'class_name' and 'bbox' (x, y, x2, y2).
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
        detected_structures = detect_objects_yolo(sample_image)
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