import psycopg2
from psycopg2.extras import RealDictCursor
import time
from .config import settings

while True:
    try:
        conn = psycopg2.connect(f"host={settings.database_hostname} dbname={settings.database_name} user={settings.database_username} password={settings.database_password}", cursor_factory=RealDictCursor)
        cur = conn.cursor()
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)
