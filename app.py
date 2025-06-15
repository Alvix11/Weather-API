from fastapi import FastAPI
from dotenv import load_dotenv
import os
import uvicorn
import httpx
import redis

app = FastAPI()

load_dotenv()
API_KEY = os.getenv('API_KEY')

BASE_URL = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/London,UK?key={API_KEY}"

r = redis.Redis(host='localhost', port=6379, db=0)
r.set('test', 'funciona')
#print(r.get('test').decode('utf-8'))

@app.get("/consume-api")
async def get_climate():
    async with httpx.AsyncClient() as client:
        response = await client.get(BASE_URL)
        data = response.json()
        return data