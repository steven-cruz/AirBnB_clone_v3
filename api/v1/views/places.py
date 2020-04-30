#!/usr/bin/python3
'''
API for Place
'''
from api.v1.views import app_views
from models import storage
from flask import jsonify
from flask import request
from flask import abort
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def all_city_places(city_id):
    '''Returns all place object by city_id in json format'''
    json_list = []

    place_list = storage.get('City', city_id)
    if place_list is None:
        abort(404)
    places = place_list.places
    for place in places:
        json_list.append(place.to_dict())
    return jsonify(json_list)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    '''Retrieves a Place from storage'''
    places = storage.get('Place', place_id)
    if places is None:
        abort(404)
    return jsonify(places.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    '''Deletes a City from storage'''
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)

    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    '''Creates an instance of Amenity and save it to storage'''
    city = storage.get('City', city_id)
    if city is None:
        abort(404)
    form = request.get_json(force=True)
    if form is None:
        abort(400, "Not a JSON")

    if "user_id" not in form:
        abort(404, "Missing user_id")

    user = storage.get(User, form.get("user_id"))
    if user is None:
        abort(404)

    if "name" not in form:
        abort(400, "Missing name")

    form["city_id"] = city_id
    new_place = Place(**form)
    storage.new(new_place)
    storage.save()
    return (jsonify(new_place.to_dict()), 201)


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    '''Updates Amenity object attribute'''
    place = storage.get('Place', place_id)
    if place is None:
        abort(404)
    form = request.get_json(force=True)
    if form is None:
        abort(400, "Not a JSON")

    for key, value in form.items():
        if key not in ["id", "user_id", "city_id", "created_at", "updated_at"]:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
