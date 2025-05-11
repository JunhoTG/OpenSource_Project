import json
import random

# 날씨별 추천 메뉴 후보
WEATHER_MENU_MAP = {
    "Clear":  ["비빔밥", "된장찌개", "불고기"],
    "Clouds": ["김치찌개", "제육볶음", "순대국"],
    "Rain":   ["칼국수", "순두부찌개", "파전"],
    "Snow":   ["삼계탕", "전골", "떡국"]
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

def recommend_menu(weather_main: str) -> list[str]:
    """
    1) weather_main에 맞는 후보 메뉴 중 이전에 안 골랐던 것을 고름
    2) 모두 고른 상태면 기록 초기화 후 다시 선택
    3) Top 3개 혹은 Top1개 (강수 등 특별 상황은 main이 다를 수 있지만,
       여기선 일단 항상 3개를 리턴하도록 해 두었음)
    """
    history = load_history()
    used = history.get(weather_main, [])
    candidates = [m for m in WEATHER_MENU_MAP.get(weather_main, []) if m not in used]

    if not candidates:
        history[weather_main] = []
        candidates = WEATHER_MENU_MAP.get(weather_main, []).copy()

    # 날씨별로 최대 3개 추천
    picks = random.sample(candidates, min(3, len(candidates)))
    history.setdefault(weather_main, []).extend(picks)
    save_history(history)
    return picks
