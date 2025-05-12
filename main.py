from weather import get_current_weather
from recommend import recommend_menu
from map import search_restaurants_by_menu

# 단국대 죽전캠퍼스 고정 좌표 & 이름
DKU_LAT = 37.3067
DKU_LON = 127.1003
LOCATION_NAME = "단국대 죽전캠퍼스"

def main():
    # 1) 날씨 조회
    weather = get_current_weather(DKU_LAT, DKU_LON)
    print(f"현재 날씨: {weather['main']} ({weather['desc']}) | 기온: {weather['temp']}℃\n")
    menus = recommend_menu(weather["main"], weather["temp"])

    # 2) 메뉴 추천
    menus = recommend_menu(weather["main"], weather["temp"])
    print("추천 메뉴:")
    for m in menus:
        print(f" - {m}")
    print()

    # 3) 메뉴별 식당 검색 & 출력
    per_menu = 3
    menu_to_rests = search_restaurants_by_menu(LOCATION_NAME, menus, per_menu=per_menu)

    print("메뉴별 추천 식당 리스트:")
    for menu, items in menu_to_rests.items():
        print(f"\n[{menu}]")
        if not items:
            print("  (검색 결과 없음)")
            continue
        for it in items:
            name = it["title"].replace("<b>","").replace("</b>","")
            addr = it["address"]
            print(f"  - {name} | {addr}")

if __name__ == "__main__":
    main()
