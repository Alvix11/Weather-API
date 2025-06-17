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
    format="%(asctime)s - %(levelname)s - %(message)s"
)

app = FastAPI()

load_dotenv()
API_KEY = os.getenv('API_KEY')
redis_client = redis.Redis(host='localhost', port=6379, db=0)

@app.get("/weather")
async def get_weather(city: str = Query(..., description="Name city")):

    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}?key={API_KEY}"
    cached = redis_client.get(city.lower())

    if cached:
        result = json.loads(cached)
        print("Devuelto de redis")
        return result
    
    else:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Could not connect to the weather service.")
        
        response_detail = handle_errors(response)
        if response_detail:
            raise HTTPException(status_code=response.status_code, detail=response_detail)
        
        else:
            data = response.json()
            if "currentConditions" not in data:
                raise HTTPException(status_code=500, detail="Unexpected response from the weather API.")
            
            temperature = fahrenheit_to_celsius(data["currentConditions"]["temp"])
            result = {
                    "Current conditions":{
                                        "city": data["resolvedAddress"],
                                        "temperature": f"{temperature}°C",
                                        "humidity": data["currentConditions"]["humidity"],
                                        "description": data["currentConditions"]["conditions"],
                                        },
                    "For the next 15 days":{    
                                            "description": data["description"],   
                                            }
                    }
            redis_client.set(city.lower(), json.dumps(result), ex=3600)
            print("devuelto de la api")
            return result

'''for key in redis_client.keys():
    value = redis_client.get(key)
    print(key.decode(), value.decode())'''

def fahrenheit_to_celsius(fahrenheit: float):
    celsius = round((fahrenheit - 32) * 5 / 9, 2)
    return celsius

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