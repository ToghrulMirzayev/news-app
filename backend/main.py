from fastapi import FastAPI
from pydantic import BaseModel
import redis
import json
import os

app = FastAPI()
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"), port=6379, decode_responses=True)


class NewsUpdate(BaseModel):
    action: str
    data: dict


@app.post("/create-news/")
async def create_news(news: NewsUpdate):
    news_data = news.dict()
    redis_client.publish("news-updates", json.dumps(news_data))
    return news_data
