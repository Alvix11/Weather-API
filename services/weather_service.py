import httpx
import logging
from utils.conversions import fahrenheit_to_celsius
from utils.errors import handle_errors
from fastapi import HTTPException

async def fetch_weather(city: str, api_key: str):
    """
    Queries the external weather API and returns the processed data.
    """
    url = f"https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline/{city}?key={api_key}"

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            logging.info("Requesting the API correctly")
    except httpx.RequestError:
        logging.error("An error occurred while connecting to the API.")
        raise HTTPException(status_code=503, detail="Could not connect to the weather service.")
    
    response_detail = handle_errors(response)
    if response_detail:
        logging.error(f"Unexpected response code {response.status_code}")
        raise HTTPException(status_code=response.status_code, detail=response_detail)
    
    data = response.json()
    if "currentConditions" not in data:
        logging.critical("The current conditions were not returned by the API.")
        raise HTTPException(status_code=500, detail="Unexpected response from the weather API.")
    
    temperature = fahrenheit_to_celsius(data["currentConditions"]["temp"])
    result = {
        "Current conditions": {
            "city": data["resolvedAddress"],
            "temperature": f"{temperature}",
            "humidity": data["currentConditions"]["humidity"],
            "description": data["currentConditions"]["conditions"],
        },
        "For the next 15 days": {
            "description": data["description"],
        }
    }
    return result