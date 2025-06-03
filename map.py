import requests, urllib.parse
from config import NAVER_CLIENT_ID, NAVER_CLIENT_SECRET

NAVER_LOCAL_URL = "https://openapi.naver.com/v1/search/local.json"
HEADERS = {
    "X-Naver-Client-Id": NAVER_CLIENT_ID,
    "X-Naver-Client-Secret": NAVER_CLIENT_SECRET
}

EXPANDED_KEYWORDS = {
    "덮밥": ["덮밥", "가츠동", "규동", "연어덮밥", "스테이크덮밥"],
    # 필요 시 다른 키워드도 확장 가능
}

def expand_keywords(menu):
    return EXPANDED_KEYWORDS.get(menu, [menu])

def search_restaurants_by_menu(location, menus, per_menu=3):
    results = {}
    for menu in menus:
        expanded = expand_keywords(menu)
        merged = []
        for keyword in expanded:
            q = urllib.parse.quote(f"{location} {keyword} 맛집")
            resp = requests.get(f"{NAVER_LOCAL_URL}?query={q}&display={per_menu}", headers=HEADERS)
            resp.raise_for_status()
            items = resp.json().get("items", [])

            for item in items[:per_menu]:
                link = f"https://map.naver.com/v5/search/{urllib.parse.quote(item.get('title', ''))}"
                
                merged.append({
                    "title": item.get("title", ""),
                    "link": link,
                    "address": item.get("address", "")
                })

        results[menu] = merged
    return results
