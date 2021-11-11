import requests
import sqlalchemy as db
from flask import Flask, request, jsonify
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base

people = [
    {
        'id': 1,
        'name': 'Ivan',
        'IQ': 100
    },
    {
        'id': 2,
        'name': 'Kirill',
        'IQ': 80
    }
]

app = Flask(__name__)

engine = create_engine('sqlite:///db.sqlite')

session = scoped_session(
    sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = session.query_property()


@app.route('/')
def start():
    requests.post("http://127.0.0.1:5000/my-api/v1.0", json={'id': 3, 'name': 'Jul', 'IQ': '155'})
    requests.delete("http://127.0.0.1:5000/my-api/v1.0", json={'id': 1})
    m = requests.get("http://127.0.0.1:5000/my-api/v1.0")
    return m.text


@app.route('/my-api/v1.0', methods=['GET'])
def get_names():
    data = request.json
    print(data)
    if not data:
        return jsonify(people), 200
    for person in people:
        if data['id'] == person['id']:
            return jsonify(person), 200

    return jsonify({'message': 'No person with this is id'}), 404


@app.route('/my-api/v1.0', methods=['POST'])
def add_name():
    new_person = request.json
    if not new_person:
        return 400
    people.append(new_person)
    return jsonify(new_person), 200


@app.route('/my-api/v1.0', methods=['PUT'])
def change_name():
    data = request.json
    if not data:
        return jsonify({'message': 'Not found'}), 404
    for person in people:
        if person['id'] == data['id']:
            person['name'] = data['name']
            person['IQ'] = data['IQ']

    return data, 200


@app.route('/my-api/v1.0', methods=['DELETE'])
def delete_person():
    data = request.json
    if not data:
        return jsonify({'message': 'Not found'}), 400
    for i in range(len(people)):
        if people[i]['id'] == data['id']:
            people.pop(i)
            return '', 200
    return data, 404


@app.teardown_appcontext
def shutdown_session(exception=None):
    session.remove()


if __name__ == "__main__":
    app.run(debug=True)
