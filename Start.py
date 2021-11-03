from collections import namedtuple

from flask import Flask, render_template, redirect, url_for, request, make_response

import folium, geopy


app = Flask(__name__)

start = True

Message = namedtuple('Message', 'text tag')
messages = []
Location = namedtuple('Latitude', 'Longitude')
locations = []


@app.route('/', methods=['GET'])
def hello_world():
    return render_template("index.html")


@app.route('/map', methods=['GET'])
def work_map():
    return render_template("Map.html")


def init_map():
    m = folium.Map(location=[50, 100], zoom_start=3)
    m.get_root().html.add_child(folium.Element("""
        <div style="position: fixed; 
             top: 10%; left: 0; width: 20%; height: 20%; 
             background-color:#6FB1F6; border:2px solid grey;z-index: 900;">
             <form method="post" action="/main/create_map">
                <input type="text" name="place">
                <button type="submit">Show point</button>
            </form>
        </div>
        """))
    return m

@app.route('/Map', methods=['GET', 'POST'])
def work_newMap():
    m = init_map()
    for location in locations:
        folium.Marker(location=[location[0], location[1]], popup=location[2], icon=folium.Icon(color='gray')).add_to(m)
    return m.get_root().render()


@app.route('/main/create_map', methods=['POST'])
def create_map():
    place = request.form['place']
    if place:
        location = geopy.Yandex(api_key="7828733b-3005-4d6d-9e56-ec722ec108f5").geocode(place)
        locations.append((location.latitude, location.longitude, place))
    return redirect(url_for('work_newMap'))


@app.route('/main', methods=['GET'])
def main():
    print(1)
    return render_template('main.html', messages=messages)


@app.route('/add_message', methods=['POST'])
def add_message():
    text = request.form['text']
    tag = request.form['tag']

    messages.append(Message(text, tag))

    return redirect(url_for('main'))


if __name__ == "__main__":
    app.run(debug=True)
