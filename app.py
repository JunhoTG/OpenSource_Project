from flask import Flask, request, jsonify, render_template
from weather import get_current_weather
from recommend import recommend_menu
from map import search_restaurants_by_menu

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_recommendation', methods=['POST'])
def get_recommendation():
    data = request.get_json()
    free_time = int(data['free_time'])
    group_size = int(data['group_size'])

    weather = get_current_weather(37.3067, 127.1003)
    menus = recommend_menu(weather["main"], weather["temp"], free_time, group_size)
    restaurants = search_restaurants_by_menu("단국대 죽전캠퍼스", menus, per_menu=3)

    return jsonify({
        "weather": weather,
        "menus": menus,
        "restaurants": restaurants
    })

if __name__ == '__main__':
    app.run(debug=True)
