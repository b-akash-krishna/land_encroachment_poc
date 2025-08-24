import geopandas as gpd
from sqlalchemy import create_engine
from geoalchemy2 import Geometry, WKBElement
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

# Define the database connection URL
db_url = "postgresql://postgres:mysecretpassword@localhost:5432/postgres"
engine = create_engine(db_url)
Session = sessionmaker(bind=engine)
session = Session()

# Define the SQLAlchemy base
Base = declarative_base()

# Define the table for your roads data
class Roads(Base):
    __tablename__ = 'roads'
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    geometry = Column(Geometry('LINESTRING', srid=4326))

    def __repr__(self):
        return f"<Roads(name='{self.name}')>"

# Create the table in the database
Base.metadata.create_all(engine)

# Read the shapefile
shapefile_path = "data/gis_boundaries/roads.shp"
roads_gdf = gpd.read_file(shapefile_path)

# Ensure the CRS is set to WGS 84 (EPSG:4326)
roads_gdf = roads_gdf.to_crs(epsg=4326)

# Insert the data into the PostgreSQL table
roads_gdf.to_postgis('roads', engine, if_exists='replace', index=False)

print("Data from roads.shp migrated to PostgreSQL successfully!")

session.close()