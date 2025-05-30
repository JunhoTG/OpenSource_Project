import requests, urllib.parse
from config import NAVER_CLIENT_ID, NAVER_CLIENT_SECRET

NAVER_LOCAL_URL = "https://openapi.naver.com/v1/search/local.json"
HEADERS = {
    "X-Naver-Client-Id": NAVER_CLIENT_ID,
    "X-Naver-Client-Secret": NAVER_CLIENT_SECRET
}

def search_restaurants_by_menu(location, menus, per_menu=3):
    results = {}
    for menu in menus:
        q = urllib.parse.quote(f"{location} {menu} 맛집")
        resp = requests.get(f"{NAVER_LOCAL_URL}?query={q}&display={per_menu}", headers=HEADERS)
        resp.raise_for_status()
        items = resp.json().get("items", [])
        results[menu] = items[:per_menu]
    return results
