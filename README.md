# Weather API Wrapper Service

A simple, modular FastAPI service that provides current weather and 15-day forecasts for any city.  
It acts as a wrapper around the Visual Crossing Weather API, caches results using Redis, and exposes a clean, developer-friendly endpoint.

---

## Features

- **/weather endpoint:** Get current weather and 15-day forecast for any city.
- **Caching:** Uses Redis to cache results and reduce external API calls.
- **Error handling:** Returns clear error messages for invalid cities, API issues, or connection problems.
- **Unit conversion:** Converts temperatures from Fahrenheit to Celsius.
- **Modular codebase:** Clean separation of concerns using services, utils, and cache modules.

---

## Project Structure

```
Weather-API/
├── app.py
├── services/
│   └── weather_service.py
├── utils/
│   ├── conversions.py
│   └── errors.py
├── cache/
│   └── redis_cache.py
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/weather-api-wrapper.git
cd weather-api-wrapper
```

### 2. Create and activate a virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Create a `.env` file in the project root:

```
API_KEY=your_visualcrossing_api_key
```

### 5. Start Redis

Make sure you have Redis running locally on port 6379.

### 6. Run the API

```bash
uvicorn app:app --reload
```

---

## Usage

- **Endpoint:**  
  `GET /weather?city=London`

- **Interactive docs:**  
  Visit [http://localhost:8000/docs](http://localhost:8000/docs)

---

## Example Response

```json
{
  "Current conditions": {
    "city": "London, England, United Kingdom",
    "temperature": "15.0",
    "humidity": 70.1,
    "description": "Partially cloudy"
  },
  "For the next 15 days": {
    "description": "Similar temperatures continuing with a chance of rain Friday, Monday & Tuesday."
  }
}
```

---

## License

MIT

---

##