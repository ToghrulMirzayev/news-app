import time
import redis
import psycopg2
import json
import os


POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")
POSTGRES_DB = os.getenv("POSTGRES_DB", "news_db")
POSTGRES_USER = os.getenv("POSTGRES_USER", "postgres")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")


redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"), port=6379, decode_responses=True)


conn = psycopg2.connect(
    dbname=POSTGRES_DB,
    user=POSTGRES_USER,
    password=POSTGRES_PASSWORD,
    host=POSTGRES_HOST,
)
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS news (
    id SERIAL PRIMARY KEY,
    data JSONB
)
""")
conn.commit()


def handle_message(message):
    if message["type"] == "message":

        data = json.loads(message["data"])

        if data.get("action") == "UPDATE":
            cursor.execute(
                "INSERT INTO news (data) VALUES (%s)",
                [json.dumps(data["data"])]
            )
            conn.commit()

            time.sleep(20)

            redis_client.publish("news-updates", json.dumps({
                "type": "NEWS_UPDATE",
                "data": data["data"]
            }))


pubsub = redis_client.pubsub()
pubsub.subscribe(**{"news-updates": handle_message})
pubsub.run_in_thread(sleep_time=0.01)
