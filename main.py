import click
from weather import get_current_weather
from recommend import recommend_menu
from map import search_restaurants_by_menu

DKU_LAT, DKU_LON = 37.3067, 127.1003
LOCATION_NAME = "단국대 죽전캠퍼스"

@click.command()
@click.option('--free-time', prompt='공강 시간 입력 (분)', type=int)
@click.option('--group-size', prompt='식사 인원 수 입력', type=int)
def main(free_time, group_size):
    weather = get_current_weather(DKU_LAT, DKU_LON)
    click.echo(f"\n🌤️ 현재 날씨: {weather['main']} ({weather['desc']}) | {weather['temp']}℃\n")

    menus = recommend_menu(weather["main"], weather["temp"], free_time, group_size)
    click.echo("🍽️ 추천 메뉴:")
    for m in menus:
        click.echo(f" - {m}")

    menu_to_rests = search_restaurants_by_menu(LOCATION_NAME, menus, per_menu=3)
    click.echo("\n📍 추천 식당 리스트:")
    for menu, items in menu_to_rests.items():
        click.echo(f"\n[{menu}]")
        if not items:
            click.echo("  (검색 결과 없음)")
            continue
        for it in items:
            name = it["title"].replace("<b>", "").replace("</b>", "")
            addr = it["address"]
            click.echo(f"  - {name} | {addr}")

if __name__ == "__main__":
    main()



