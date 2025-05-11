import requests
from config import OPENWEATHER_KEY

def get_current_weather(lat: float, lon: float) -> dict:
    """
    고정된 좌표(lat, lon)로부터 현재 날씨(main, description)를 가져옵니다.
    """
    url = (
        "https://api.openweathermap.org/data/2.5/weather"
        f"?lat={lat}&lon={lon}&appid={OPENWEATHER_KEY}"
        "&units=metric&lang=kr"
    )
    resp = requests.get(url)
    resp.raise_for_status()
    data = resp.json()
    return {
        "main": data["weather"][0]["main"],       # e.g. "Clear", "Rain"
        "desc": data["weather"][0]["description"] # e.g. "맑음", "가벼운 비"
    }
