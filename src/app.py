"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, People, Planets, Favorite_People, Favorite_Planets
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False

db_url = os.getenv("DATABASE_URL")
if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

MIGRATE = Migrate(app, db)
db.init_app(app)
CORS(app)
setup_admin(app)

# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

# generate sitemap with all your endpoints
@app.route('/')
def sitemap():
    return generate_sitemap(app)



# =================================== Methods =================================

# PEOPLE
@app.route('/people', methods=['GET'])
def get_people():
    people = People.query.all()
    all_people = list(map(lambda person: person.serialize(), people))

    response_body = {
        "msg": "GET /people response",
        "people": all_people
    }
    return jsonify(response_body), 200


@app.route('/people/<int:people_id>', methods=['GET'])
def get_people_by_id(people_id):
    people = People.query.filter_by(id=people_id)
    person_details = list(map(lambda person: person.serialize(), people))

    if person_details == []:
        raise APIException('Person not found ', status_code=404)

    response_body = {
        "msg": "GET /people/<int:people_id> response",
        "person": person_details
    }
    return jsonify(response_body), 200


# PLANETS
@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planets.query.all()
    all_planets = list(map(lambda planet: planet.serialize(), planets))

    response_body = {
        "msg": "GET /planets response",
        "users": all_planets
    }
    return jsonify(response_body), 200


@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planets_details(planet_id):
    planet_by_id = Planets.query.filter_by(id=planet_id)
    planet_details = list(map(lambda planet: planet.serialize(), planet_by_id))

    if planet_details == []:
        raise APIException('Planet not found', status_code=404)

    response_body = {
        "msg": "GET /planets/<int:planet_id> response",
        "result": planet_details
    }
    return jsonify(response_body), 200


# USER
@app.route('/user', methods=['GET'])
def get_users():
    users = User.query.all()
    all_users = list(map(lambda user: user.serialize(), users))

    response_body = {
        "msg": "GET /user response",
        "users": all_users
    }
    return jsonify(response_body), 200


@app.route('/user/favorites', methods=['GET'])
def get_user_favorites():
    request_body = request.get_json(force=True)

    if "user_id" not in request_body:
        raise APIException('Please enter the user_id', status_code=404)

    favorite_people = Favorite_People.query.filter_by(id_user=request_body['user_id'])
    all_favorite_people = list(
        map(lambda people: people.serialize(), favorite_people))
    
    favorite_planets = Favorite_Planets.query.filter_by(id_user=request_body['user_id'])
    all_favorite_planets = list(
        map(lambda planet: planet.serialize(), favorite_planets))

    response_body = {
        "msg": "GET /user/favorites response",
        "favorites": {"people": all_favorite_people,
                      "planets": all_favorite_planets,
                      }
    }
    return jsonify(response_body), 200


# FAVORITES POSTS
@app.route('/favorite/planet/<int:planet_id>', methods=['POST'])
def add_favorite_planets(planet_id):
    request_body = request.get_json(force=True)

    if "user_id" not in request_body:
        raise APIException('Please enter the user_id', status_code=404)

    favorite_planets = Favorite_Planets(
        id_user = request_body['user_id'],
        id_planet = planet_id
    )

    favorite_planets.save()

    response_body = {
        "msg": "POST /favorite/planet/<int:planet_id> response",
        "result": request_body
    }
    return jsonify(response_body), 201


@app.route('/favorite/people/<int:people_id>', methods=['POST'])
def add_favorite_people(people_id):
    request_body = request.get_json(force=True)

    if "user_id" not in request_body:
        raise APIException('Please enter the user_id', status_code=404)

    favorite_people = Favorite_People(
        id_user = request_body['user_id'],
        id_people = people_id
    )

    favorite_people.save()

    response_body = {
        "msg": "POST /favorite/people/<int:people_id> response",
        "result": request_body
    }
    return jsonify(response_body), 201


# FAVORITES DELETE
@app.route('/favorite/planet/<int:planet_id>', methods=['DELETE'])
def delete_favorite_planets(planet_id):
    request_body = request.get_json(force=True)

    if "user_id" not in request_body:
        raise APIException('Please enter the user_id', status_code=404)
    
    favorite_planets = Favorite_Planets.query.filter_by(
    id_user=request_body['user_id'], id_planet=planet_id)

    all_planets = list(map(lambda planet: planet, favorite_planets))

    if all_planets == []:
        raise APIException('Favorite planet not found', status_code=404)

    favorite_planets = all_planets[0]
    favorite_planets.delete()

    reponse_body = {
        "msg": "DELETE /favorite/planet/<int:planet_id> response",
        "status": "done"
    }
    return jsonify(reponse_body), 200 


@app.route('/favorite/people/<int:people_id>', methods=['DELETE'])
def delete_favorite_people(people_id):
    request_body = request.get_json(force=True)

    if "user_id" not in request_body:
        raise APIException('Please enter the user_id', status_code=404)

    favorite_people = Favorite_People.query.filter_by(
        id_user=request_body['user_id'], id_people=people_id)
    
    all_people = list(map(lambda people: people, favorite_people))

    if all_people == []:
        raise APIException('Favorite people not found', status_code=404)

    favorite_people = all_people[0]
    favorite_people.delete()

    reponse_body = {
        "msg": "DELETE /favorite/people/<int:people_id> response",
        "status": "done"
    }
    return jsonify(reponse_body), 200


# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
