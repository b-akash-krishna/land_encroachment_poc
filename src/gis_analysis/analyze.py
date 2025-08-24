import geopandas as gpd
from shapely.geometry import box, Point
import os

def check_encroachments(detections, road_shp_path):
    """
    Compares detected objects with road boundaries to find encroachments.

    Args:
        detections (list): A list of detected object dictionaries.
        road_shp_path (str): Path to the road network shapefile.
        
    Returns:
        list: A list of dictionaries for each encroachment found.
    """
    if not os.path.exists(road_shp_path):
        print(f"Error: Road shapefile not found at {road_shp_path}")
        return []

    # Load road data
    roads_gdf = gpd.read_file(road_shp_path, driver='ESRI Shapefile')
    
    # Create a buffer around the roads to simulate public land
    road_buffer = roads_gdf.geometry.buffer(0.0005) # Note: Buffer size is in degrees for a simple geographic CRS
    
    encroachments = []
    
    for det in detections:
        x1, y1, x2, y2 = det['bbox']
        # Create a Polygon from the bounding box
        # We simulate the GIS geometry from the pixel bbox
        bbox_polygon = box(x1, y1, x2, y2)
        
        # Check for intersection
        # The .any() method returns True if any object intersects the buffer
        if road_buffer.intersects(bbox_polygon).any():
            # Find the nearest road segment for reporting
            road_segment = roads_gdf[road_buffer.intersects(bbox_polygon)].iloc[0]
            
            encroachments.append({
                "type": det['class_name'],
                "bbox": det['bbox'],
                "location": str(bbox_polygon.centroid),
                "affected_area_sq_m": bbox_polygon.area,
                "nearest_boundary_id": road_segment.get('name', 'Unnamed Road')
            })
            
    return encroachments

if __name__ == "__main__":
    # # Example usage
    # # Simulate a few detections for testing
    # test_detections = [
    #     {'class_name': 'building', 'bbox': [100, 100, 150, 150]},
    #     {'class_name': 'shed', 'bbox': [500, 500, 550, 550]}
    # ]
    test_detections = [
    # This bbox is designed to overlap with your dummy road's coordinates
    # Bbox in pixel coordinates, but for our simplified test, we'll use degrees
    {'class_name': 'building', 'bbox': [-74.006, 40.7128, -73.985, 40.7580]},
    {'class_name': 'shed', 'bbox': [-74.007, 40.7127, -74.005, 40.7129]}
    ]
    
    # Corrected path to the shapefile relative to this script
    road_path = "../../data/gis_boundaries/roads.shp"
    
    if os.path.exists(road_path):
        found_encroachments = check_encroachments(test_detections, road_path)
        print("Found encroachments:", found_encroachments)
    else:
        print("Road shapefile not found. Please create one with QGIS.")