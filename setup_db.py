import psycopg2
from psycopg2 import sql

def setup_postgis_db():
    try:
        # Connect to the PostgreSQL database
        conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="mysecretpassword",
            host="localhost",
            port="5432"
        )
        conn.autocommit = True
        cur = conn.cursor()

        # Check if the PostGIS extension is installed
        print("Checking for PostGIS extension...")
        cur.execute("SELECT postgis_version();")
        print(f"PostGIS version: {cur.fetchone()[0]}")
        print("PostGIS is installed and ready to use.")

    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")
        print("Please ensure your PostgreSQL/PostGIS Docker container is running.")
    finally:
        if conn:
            cur.close()
            conn.close()

if __name__ == "__main__":
    setup_postgis_db()