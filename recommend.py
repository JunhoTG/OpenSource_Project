import json
import random

# 날씨별 추천 메뉴 후보
WEATHER_TEMP_MENU_MAP = {
    "Clear": {
        "cold":  ["우동", "부대찌개", "라멘"],
        "mild":  ["비빔밥", "된장찌개", "불고기"],
        "hot":   ["냉면", "쫄면", "콩국수"]
    },
    "Clouds": {
        "cold":  ["김치찜", "감자탕", "수제비"],
        "mild":  ["김치찌개", "제육볶음", "순대국"],
        "hot":   ["비빔국수", "열무국수", "냉콩국"]
    },
    "Rain": {
        "cold":  ["칼국수", "수제비", "전골"],
        "mild":  ["파전", "순두부찌개", "우동"],
        "hot":   ["냉모밀", "밀면", "잔치국수"]
    }
}

HISTORY_FILE = "history.json"

def load_history() -> dict:
    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def save_history(history: dict):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def get_temp_range(temp: float) -> str:
    if temp < 15:
        return "cold"
    elif temp < 25:
        return "mild"
    else:
        return "hot"

def recommend_menu(weather_main: str, temp: float) -> list[str]:
    temp_range = get_temp_range(temp)
    history = load_history()
    used = history.get(f"{weather_main}_{temp_range}", [])

    candidates = [
        m for m in WEATHER_TEMP_MENU_MAP.get(weather_main, {}).get(temp_range, [])
        if m not in used
    ]

    if not candidates:
        history[f"{weather_main}_{temp_range}"] = []
        candidates = WEATHER_TEMP_MENU_MAP.get(weather_main, {}).get(temp_range, []).copy()

    picks = random.sample(candidates, min(3, len(candidates)))
    history.setdefault(f"{weather_main}_{temp_range}", []).extend(picks)
    save_history(history)
    return picks
