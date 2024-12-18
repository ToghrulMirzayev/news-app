from fastapi import FastAPI
from pydantic import BaseModel
import redis
import json
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi import Request
from fastapi.responses import FileResponse
import os

app = FastAPI()
redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"), port=6379, decode_responses=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.mount("/static", StaticFiles(directory="frontend/static"), name="static")


class NewsUpdate(BaseModel):
    action: str
    data: dict

@app.get("/")
async def root():
    return FileResponse(os.path.join("frontend/static", "index.html"))


@app.post("/create-news/")
async def create_news(news: NewsUpdate, request: Request):
    print("Request received:", await request.body())
    news_data = news.dict()
    redis_client.publish("news-updates", json.dumps(news_data))
    return news_data
