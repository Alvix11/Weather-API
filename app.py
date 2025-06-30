from fastapi import FastAPI, Query, HTTPException
from dotenv import load_dotenv
import os
import json
import logging
from cache.redis_cache import redis_client
from services.weather_service import fetch_weather

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s"
)

app = FastAPI()

load_dotenv()
API_KEY = os.getenv('API_KEY')

@app.get("/weather")
async def get_weather(city: str = Query(..., description="Name city")):
    """
    Returns the current weather and the 15-day forecast for the specified city.
    Uses Redis for caching and handles errors from the external API.
    """
    if not city or not city.strip():
        raise HTTPException(status_code=400, detail="City parameter cannot be empty.")

    city_key = city.strip().lower()
    cached = redis_client.get(city_key)

    if cached:
        result = json.loads(cached)
        logging.info("Information obtained from Redis")
        return result

    # If not in cache, queries the external API.
    result = await fetch_weather(city, API_KEY)
    redis_client.set(city_key, json.dumps(result), ex=3600)
    logging.info("Information obtained from API and cached")
    return result