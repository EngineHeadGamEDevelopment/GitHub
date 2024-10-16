import requests
import asyncio
import os
import json
from datetime import datetime
from tkinter import messagebox

DATA_PATH = 'data'

API_KEYS = {
    'weather': "8db9fee751e3fa5a3596c9cc96486f91",
    'news': "e18eb01c2b3d45908104628792035eeb",
    'geological': "ee8f7ba8bbfed94c77099072bd5be2d9",
    'currency': "2b908120946bfb453a18339c",
    'stock': "D8WS72X9TI9FZMH7",
    'timezone': "5KJZ0PM66RNQ"
}

def save_data(data, filename):
    """Save data to a JSON file."""
    try:
        with open(os.path.join(DATA_PATH, filename), 'w') as f:
            json.dump(data, f, indent=4)
    except IOError as e:
        messagebox.showerror("Error", f"Could not save data: {e}")

async def fetch_weather(city):
    """Fetch weather data."""
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEYS['weather']}&units=metric"
    response = await asyncio.to_thread(requests.get, url)
    return response.json() if response.status_code == 200 else None

# Other API methods can be added similarly (news, geological, currency, etc.)
