from fastapi import FastAPI, Query
from dotenv import load_dotenv
import os
import uvicorn
import httpx
import redis

app = FastAPI()

load_dotenv()
API_KEY = os.getenv('API_KEY')

@app.get("/weather")
async def get_weather(city: str = Query(..., description="Name city")):
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}?key={API_KEY}"
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        data = response.json()

        result = {
                "city": city,
                "temperature": data["currentConditions"]["temp"],
                "description": data["currentConditions"]["conditions"]
                }
        return result