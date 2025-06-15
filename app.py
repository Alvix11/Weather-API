from fastapi import FastAPI, Query
from dotenv import load_dotenv
import os
import redis.client
import uvicorn
import httpx
import redis
import json

app = FastAPI()

load_dotenv()
API_KEY = os.getenv('API_KEY')
redis_client = redis.Redis(host='localhost', port=6379, db=0)

@app.get("/weather")
async def get_weather(city: str = Query(..., description="Name city")):
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}?key={API_KEY}"
    cached = redis_client.get(city)
    if cached:
        result = json.loads(cached)
        print("Devuelto de redis")
        return result
    else:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            data = response.json()

            result = {
                    "city": city,
                    "temperature": data["currentConditions"]["temp"],
                    "description": data["currentConditions"]["conditions"]
                    }

            redis_client.set(city, json.dumps(result))
            print("devuelto de la api")
            return result