import json
import random

WEATHER_TEMP_MENU_MAP = {
    "Clear": {
        "cold": [
            "라멘", "우동", "칼국수", "된장찌개", "순두부찌개",
            "떡국", "부대찌개", "소고기무국", "김치찌개", "감자국"
        ],
        "mild": [
            "비빔밥", "불고기", "제육볶음", "돈까스", "김치찌개",
            "된장찌개", "덮밥", "파스타", "카레", "햄버거"
        ],
        "hot": [
            "냉면", "쫄면", "비빔국수", "콩국수", "냉모밀",
            "열무국수", "냉우동", "샐러드", "햄버거", "김밥"
        ]
    },
    "Clouds": {
        "cold": [
            "감자탕", "순대국", "김치찜", "전골", "수제비",
            "부대찌개", "된장찌개", "갈비탕", "닭개장", "우거지해장국"
        ],
        "mild": [
            "제육볶음", "불고기", "김치찌개", "카레", "돈까스",
            "비빔밥", "칼국수", "덮밥", "순두부찌개", "피자", "햄버거"
        ],
        "hot": [
            "비빔국수", "쫄면", "콩국수", "냉면", "열무국수",
            "밀면", "냉모밀", "파스타", "빙수", "피자"
        ]
    },
    "Rain": {
        "cold": [
            "수제비", "칼국수", "부대찌개", "감자탕", "전골",
            "샤브샤브", "김치전골", "해물순두부", "우동", "닭한마리"
        ],
        "mild": [
            "덮밥", "김치찌개", "순두부찌개", "제육볶음", "라멘",
            "우동", "된장찌개", "불고기", "카레", "햄버거"
        ],
        "hot": [
            "밀면", "냉모밀", "쫄면", "비빔국수", "잔치국수",
            "콩국수", "냉비빔우동", "열무국수", "빙수"
        ]
    }
}

def get_temp_range(temp):
    return "cold" if temp < 15 else "mild" if temp < 25 else "hot"

def load_json(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)

def load_history():
    try:
        return load_json("history.json")
    except FileNotFoundError:
        return {}

def save_history(history):
    with open("history.json", "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

def filter_menus(menus, filename, category):
    menu_map = load_json(filename)
    filtered = [m for m in menus if m in menu_map.get(category, [])]
    return filtered if filtered else menus

def recommend_menu(weather_main, temp, free_time, group_size):
    temp_range = get_temp_range(temp)
    history = load_history()
    key = f"{weather_main}_{temp_range}"

    # 날씨/온도 기반 후보
    base_candidates = WEATHER_TEMP_MENU_MAP.get(weather_main, {}).get(temp_range, [])
    if not base_candidates:
        return ["비빔밥", "된장찌개", "불고기"]  # fallback

    # 인원 필터용 그룹 분류
    group_category = (
        "single" if group_size == 1 else
        "small_group" if group_size <= 4 else
        "large_group"
    )

    def filter_menus(menus, filename, category):
        menu_map = load_json(filename)
        return [m for m in menus if m in menu_map.get(category, [])]

    # 공강시간 조건 처리
    def filter_time(menus):
        if free_time >= 120:
            return menus  # 시간 조건 무시
        time_category = "short" if free_time < 60 else "medium" if free_time < 120 else "long"
        return filter_menus(menus, "menu_time.json", time_category)

    # 조건 완화 순서대로 필터링
    filter_steps = [
        lambda menus: filter_menus(filter_time(menus), "menu_group.json", group_category),
        lambda menus: filter_time(menus),  # 인원수 무시
        lambda menus: filter_menus(menus, "menu_group.json", group_category),  # 시간 무시
        lambda menus: menus  # 둘 다 무시
    ]

    candidates = []
    for step in filter_steps:
        candidates = step(base_candidates)
        if candidates:
            break

    # fallback
    if not candidates:
        return []

    used = set(history.get(key, []))
    final_candidates = set(candidates) - used
    if not final_candidates:
        used.clear()
        final_candidates = set(candidates)

    picks = random.sample(list(final_candidates), min(3, len(final_candidates)))

    used.update(picks)
    history[key] = list(used)
    save_history(history)

    return picks




