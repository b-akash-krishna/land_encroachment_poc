from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
import os
import json

def generate_pdf_report(encroachments, output_path="../../reports/encroachment_report.pdf"):
    """
    Generates a PDF report from a list of encroachment data.

    Args:
        encroachments (list): A list of dictionaries with encroachment details.
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
        for i, enc in enumerate(encroachments):
            story.append(Paragraph(f"<b>Encroachment #{i+1}</b>", styles['h2']))
            story.append(Paragraph(f"<b>Type:</b> {enc['type']}", styles['Normal']))
            story.append(Paragraph(f"<b>Location:</b> {enc['location']}", styles['Normal']))
            story.append(Paragraph(f"<b>Area Affected:</b> {enc['affected_area_sq_m']:.2f} sq m", styles['Normal']))
            story.append(Paragraph(f"<b>Nearest Boundary:</b> {enc['nearest_boundary_id']}", styles['Normal']))
            story.append(Spacer(1, 12))
            
    doc.build(story)
    return output_path

if __name__ == "__main__":
    # Example usage with dummy data
    dummy_data = [
        {"type": "building", "location": "POINT (10.025 76.31)", "affected_area_sq_m": 50, "nearest_boundary_id": "Main Road"},
        {"type": "fence", "location": "POINT (10.019 76.29)", "affected_area_sq_m": 15, "nearest_boundary_id": "Bypass Road"}
    ]
    generate_pdf_report(dummy_data)
    print("PDF report generated successfully.")