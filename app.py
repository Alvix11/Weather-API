from fastapi import FastAPI, Query, HTTPException
from dotenv import load_dotenv
import os
import redis.client
import uvicorn
import httpx
import redis
import json
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s - %(message)s"
)

app = FastAPI()

load_dotenv()
API_KEY = os.getenv('API_KEY')
redis_client = redis.Redis(host='localhost', port=6379, db=0)

@app.get("/weather")
async def get_weather(city: str = Query(..., description="Name city")):

    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}?key={API_KEY}"
    cached = redis_client.get(city.strip().lower())

    if cached:
        result = json.loads(cached)
        logging.info("Information obtained from Redis")
        return result
    
    else:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                logging.info("Requesting the API correctly")
        except httpx.RequestError:
            logging.warning("An error occurred while connecting to the API.")
            raise HTTPException(status_code=503, detail="Could not connect to the weather service.")
        
        response_detail = handle_errors(response)
        if response_detail:
            logging.info(f"Unexpected response code {response.status_code}")
            raise HTTPException(status_code=response.status_code, detail=response_detail)
        
        else:
            data = response.json()
            if "currentConditions" not in data:
                logging.critical("The current conditions were not returned by the API.")
                raise HTTPException(status_code=500, detail="Unexpected response from the weather API.")
            
            temperature = fahrenheit_to_celsius(data["currentConditions"]["temp"])
            result = {
                    "Current conditions":{
                                        "city": data["resolvedAddress"],
                                        "temperature": f"{temperature}",
                                        "humidity": data["currentConditions"]["humidity"],
                                        "description": data["currentConditions"]["conditions"],
                                        },
                    "For the next 15 days":{    
                                            "description": data["description"],   
                                            }
                    }
            redis_client.set(city.strip().lower(), json.dumps(result), ex=3600)
            logging.info("Information obtained from API")
            return result

'''for key in redis_client.keys():
    value = redis_client.get(key)
    print(key.decode(), value.decode())'''

def fahrenheit_to_celsius(fahrenheit: float):
    try:
        celsius = round((fahrenheit - 32) * 5 / 9, 2)
        logging.info(f"Converted {fahrenheit}F to {celsius}C")
        return celsius
    except Exception as e:
        logging.info(f"Unexpected error in converting Fahrenheit to Celsius: {e}")
        return fahrenheit

def handle_errors(response):
    if response.status_code == 404:
        return "Page not found"
    elif response.status_code == 500:
        return "A general error occurred while processing the request."
    elif response.status_code == 400:
        return "The format of the API is incorrect or an invalid parameter or combination of parameters was supplied."
    elif response.status_code == 401:
        return"There is a problem with the API key, account or subscription."
    elif response.status_code == 429:
        return "The account has exceeded their assigned limits."
    elif response.status_code != 200:
        return f"Unexpected error: {response.status_code}"
    return None
        
#redis_client.flushdb()