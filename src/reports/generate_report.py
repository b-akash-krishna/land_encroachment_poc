from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet
import os
import json
import cv2
from PIL import Image as PILImage
from reportlab.lib.utils import ImageReader

def create_composite_image(image_path, detections, output_path):
    """
    Creates a composite image with bounding boxes drawn on it.
    
    Args:
        image_path (str): Path to the original image.
        detections (list): List of detected objects with bounding boxes.
        output_path (str): Path to save the new image.
    """
    img = cv2.imread(image_path)
    
    for det in detections:
        # Assuming bbox is in pixel coordinates for drawing
        if 'bbox' in det:
            bbox = det['bbox']
            x1, y1, x2, y2 = map(int, bbox)
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.putText(img, det['class_name'], (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    cv2.imwrite(output_path, img)

def generate_pdf_report(encroachments, original_image_path, output_path="reports/encroachment_report.pdf"):
    """
    Generates a PDF report from a list of encroachment data with image overlays.

    Args:
        encroachments (list): A list of dictionaries with encroachment details.
        original_image_path (str): Path to the original image used for detection.
        output_path (str): The path to save the PDF.

    Returns:
        str: The path to the generated PDF file.
    """
    # Create the reports directory if it doesn't exist
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Title
    story.append(Paragraph("<b>Land Encroachment Report</b>", styles['Title']))
    story.append(Spacer(1, 12))

    if not encroachments:
        story.append(Paragraph("No encroachments detected.", styles['Normal']))
    else:
        # Create a list of all detected bboxes to pass to image creator
        all_detections = []
        for enc in encroachments:
            all_detections.append({
                "class_name": enc['type'],
                "bbox": enc.get('bbox', [0,0,0,0]) # Use a dummy bbox if none is found
            })

        # Generate a composite image with bounding boxes
        temp_image_path = "temp_uploads/composite_image.jpg"
        create_composite_image(original_image_path, all_detections, temp_image_path)

        # Add the composite image to the story
        if os.path.exists(temp_image_path):
            img_width, img_height = PILImage.open(temp_image_path).size
            # Scale the image to fit the page
            img_ratio = img_width / img_height
            page_width = 500
            img = Image(temp_image_path, width=page_width, height=page_width / img_ratio)
            story.append(img)
            story.append(Spacer(1, 12))

        # Add details for each encroachment
        for i, enc in enumerate(encroachments):
            story.append(Paragraph(f"<b>Encroachment #{i+1}</b>", styles['h2']))
            story.append(Paragraph(f"<b>Type:</b> {enc['type']}", styles['Normal']))
            story.append(Paragraph(f"<b>Location:</b> {enc['location']}", styles['Normal']))
            story.append(Paragraph(f"<b>Affected Area:</b> {enc['affected_area_sq_m']:.2f} sq m", styles['Normal']))
            story.append(Paragraph(f"<b>Nearest Boundary:</b> {enc['nearest_boundary_id']}", styles['Normal']))
            story.append(Spacer(1, 12))
            
    doc.build(story)
    return output_path

if __name__ == "__main__":
    # Example usage with dummy data and a sample image
    dummy_data = [
        {"type": "building", "location": "POINT (10.025 76.31)", "affected_area_sq_m": 50, "nearest_boundary_id": "Main Road", "bbox": [100, 100, 150, 150]},
        {"type": "fence", "location": "POINT (10.019 76.29)", "affected_area_sq_m": 15, "nearest_boundary_id": "Bypass Road", "bbox": [500, 500, 550, 550]}
    ]
    
    # You need a sample image to test this
    sample_image = "../../data/aerial_images/frame_0.jpg"
    generate_pdf_report(dummy_data, sample_image)
    print("PDF report with image generated successfully.")