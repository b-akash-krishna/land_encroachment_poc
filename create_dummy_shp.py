import geopandas as gpd
from shapely.geometry import LineString, Point
import os

def create_dummy_shapefile():
    """
    Creates a simple dummy shapefile for testing purposes.
    """
    # Define the CRS (Coordinate Reference System)
    # EPSG:4326 is WGS 84, a standard geographic CRS used for web maps
    crs = "EPSG:4326"

    # Create a sample LineString to represent a road
    # Coordinates are in (longitude, latitude) format
    line = LineString([(-74.006, 40.7128), (-73.985, 40.7580), (-73.96, 40.78)])

    # Create a GeoDataFrame with the explicit CRS
    gdf = gpd.GeoDataFrame({
        'name': ['Main Road'],
        'geometry': [line]
    }, crs=crs)

    # Define the output path
    output_dir = "land_encroachment_poc\data\gis_boundaries"
    output_path = os.path.join(output_dir, "roads.shp")

    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Save the GeoDataFrame to a shapefile
    # This will create multiple files (e.g., .shp, .shx, .dbf)
    gdf.to_file(output_path, driver='ESRI Shapefile')

    print(f"Dummy shapefile created at: {output_path}")

if __name__ == "__main__":
    create_dummy_shapefile()