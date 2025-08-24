import geopandas as gpd
from sqlalchemy import create_engine
from shapely.geometry import box
import os

# Database connection URL
db_url = "postgresql://postgres:mysecretpassword@localhost:5432/postgres"

def check_encroachments(detections):
    """
    Compares detected objects with road boundaries from the database to find encroachments.

    Args:
        detections (list): A list of detected object dictionaries.
        
    Returns:
        list: A list of dictionaries for each encroachment found.
    """
    # Load road data directly from the PostGIS database
    engine = create_engine(db_url)
    roads_gdf = gpd.read_postgis("SELECT name, geometry FROM roads", engine, geom_col='geometry')
    
    # Create a buffer around the roads
    road_buffer = roads_gdf.geometry.buffer(0.0005) 
    
    encroachments = []
    
    for det in detections:
        # Check if geographic bbox is available
        if 'geographic_bbox' in det:
            lon1, lat1, lon2, lat2 = det['geographic_bbox']
            bbox_polygon = box(lon1, lat1, lon2, lat2)
        else:
            x1, y1, x2, y2 = det['bbox']
            bbox_polygon = box(x1, y1, x2, y2)
        
        # Check for intersection
        if road_buffer.intersects(bbox_polygon).any():
            road_segment = roads_gdf[road_buffer.intersects(bbox_polygon)].iloc[0]
            
            encroachments.append({
                "type": det['class_name'],
                "location": str(bbox_polygon.centroid),
                "affected_area_sq_m": bbox_polygon.area,
                "nearest_boundary_id": road_segment.get('name', 'Unnamed Road')
            })
            
    return encroachments

if __name__ == "__main__":
    # Example usage with dummy data
    test_detections = [
        {'class_name': 'building', 'geographic_bbox': [-74.006, 40.7128, -73.985, 40.7580]},
        {'class_name': 'shed', 'geographic_bbox': [-74.007, 40.7127, -74.005, 40.7129]}
    ]
    
    found_encroachments = check_encroachments(test_detections)
    print("Found encroachments:", found_encroachments)