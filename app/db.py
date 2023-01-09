import psycopg2
from psycopg2.extras import RealDictCursor
import time

while True:
    try:
        conn = psycopg2.connect("host=localhost dbname=python-api user=postgres password=admin", cursor_factory=RealDictCursor)
        cur = conn.cursor()
        break
    except Exception as error:
        print("Connecting to database failed")
        print("Error: ", error)
        time.sleep(2)

