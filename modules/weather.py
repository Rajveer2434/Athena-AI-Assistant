import requests

API_KEY = "0495f68aa5a160bacd79a17e624eeab7"

def get_weather(city):

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"

    data = requests.get(url).json()

    return {
        "temp": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "condition": data["weather"][0]["main"]
    }