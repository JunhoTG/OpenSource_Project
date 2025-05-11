import urllib.parse
import requests
from config import NAVER_CLIENT_ID, NAVER_CLIENT_SECRET

NAVER_LOCAL_URL = "https://openapi.naver.com/v1/search/local.json"
HEADERS = {
    "X-Naver-Client-Id": NAVER_CLIENT_ID,
    "X-Naver-Client-Secret": NAVER_CLIENT_SECRET
}

def search_restaurants_by_menu(location: str,
                               menus: list[str],
                               per_menu: int = 3,
                               display: int = 5) -> dict[str, list[dict]]:
    """
    location + 각 메뉴 키워드로 '맛집' 리뷰순 검색을 수행합니다.
    반환값은 {메뉴: [식당아이템,...]} 형태의 dict입니다.
      - per_menu: 메뉴당 실제로 담을 식당 개수
      - display: API 호출 시 최대 조회 개수
    """
    results: dict[str, list[dict]] = {}
    for menu in menus:
        raw_q = f"{location} {menu} 맛집"
        q = urllib.parse.quote(raw_q)
        params = f"sort=comment&query={q}&display={display}"
        resp = requests.get(f"{NAVER_LOCAL_URL}?{params}", headers=HEADERS)
        resp.raise_for_status()
        items = resp.json().get("items", [])
        # 메뉴별 Top per_menu개로 잘라서 저장
        results[menu] = items[:per_menu]
    return results
