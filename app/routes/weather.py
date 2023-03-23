import os
import requests
from flask import Blueprint, jsonify

if os.getenv("FLASK_DEBUG"):
    WEATHER_API_KEY = "TEST"
else:
    WEATHER_API_KEY = os.getenv("WEATHER_API_KEY", default="TEST")

weather_routes = Blueprint("weather_routes", __name__, url_prefix="/")


@weather_routes.route("weather/<city>", methods=["GET"])
def get_weather(city):

    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        city_name = data["name"]
        temperature = data["main"]["temp"]
        weather = data["weather"][0]["description"]
        return jsonify(
            {"temperature": temperature, "weather": weather, "name": city_name}
        )
    else:
        return (
            jsonify({"error": "Could not retrieve weather data."}),
            response.status_code,
        )
