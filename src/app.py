"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin
from models import db, User, Character, Planet, Favorite
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

# [GET] /people
@app.route('/people', methods=['GET'])
def get_people():
    characters = Character.query.all()
    return jsonify([character.serialize() for character in characters]), 200

# [GET] /people/<int:people_id>
@app.route('/people/<int:people_id>', methods=['GET'])
def get_person(people_id):
    character = Character.query.get(people_id)
    if not character:
        return jsonify({"error": "Character not found"}), 404
    return jsonify(character.serialize()), 200

# [GET] /planets
@app.route('/planets', methods=['GET'])
def get_planets():
    planets = Planet.query.all()
    return jsonify([planet.serialize() for planet in planets]), 200

# [GET] /planets/<int:planet_id>
@app.route('/planets/<int:planet_id>', methods=['GET'])
def get_planet(planet_id):
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"error": "Planet not found"}), 404
    return jsonify(planet.serialize()), 200

# [GET] /users
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200

# [GET] /users/<int:user_id>/favorites
@app.route('/users/<int:user_id>/favorites', methods=['GET'])
def get_user_favorites_by_id(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    favorites = Favorite.query.filter_by(user_id=user.id).all()
    return jsonify([favorite.serialize() for favorite in favorites]), 200

# [POST] /favorite/planet/<int:planet_id>/<int:user_id>
@app.route('/favorite/planet/<int:planet_id>/<int:user_id>', methods=['POST'])
def add_favorite_planet_for_user(planet_id, user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    planet = Planet.query.get(planet_id)
    if not planet:
        return jsonify({"error": "Planet not found"}), 404
    favorite = Favorite(user_id=user.id, planet_id=planet_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify(favorite.serialize()), 201

# [POST] /favorite/people/<int:people_id>/<int:user_id>
@app.route('/favorite/people/<int:people_id>/<int:user_id>', methods=['POST'])
def add_favorite_character_for_user(people_id, user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    character = Character.query.get(people_id)
    if not character:
        return jsonify({"error": "Character not found"}), 404
    favorite = Favorite(user_id=user.id, character_id=people_id)
    db.session.add(favorite)
    db.session.commit()
    return jsonify(favorite.serialize()), 201

# [DELETE] /favorite/planet/<int:planet_id>/<int:user_id>
@app.route('/favorite/planet/<int:planet_id>/<int:user_id>', methods=['DELETE'])
def delete_favorite_planet_for_user(planet_id, user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    favorite = Favorite.query.filter_by(user_id=user.id, planet_id=planet_id).first()
    if not favorite:
        return jsonify({"error": "Favorite not found"}), 404
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"message": "Favorite deleted"}), 200

# [DELETE] /favorite/people/<int:people_id>/<int:user_id>
@app.route('/favorite/people/<int:people_id>/<int:user_id>', methods=['DELETE'])
def delete_favorite_character_for_user(people_id, user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    favorite = Favorite.query.filter_by(user_id=user.id, character_id=people_id).first()
    if not favorite:
        return jsonify({"error": "Favorite not found"}), 404
    db.session.delete(favorite)
    db.session.commit()
    return jsonify({"message": "Favorite deleted"}), 200

if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
