import psycopg2
from config import config

def connect():
    conn = None
    try:
        params = config()
        conn = psycopg2.connect(**params)
        print("Connection successful!")
        return conn
    except Exception as e:
        print(f"Connection error: {e}")
        return None

if __name__ == "__main__":
    connect()