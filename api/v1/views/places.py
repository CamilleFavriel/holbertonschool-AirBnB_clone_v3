#!/usr/bin/python3
"""Places objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.place import Place
from models.city import City
from models.user import User


@app_views.route('/cities/<city_id>/places',
                 methods=['GET'], strict_slashes=False)
def places_by_city_id(city_id):
    """Retrieves the list of all Place objects of a City"""
    obj_place = storage.get(City, city_id)
    if obj_place is None:
        abort(404)

    """Get the list of place associated with the City object"""
    all_place_list = obj_place.places

    place_list = []
    """Convert each place to a dictionary"""
    for place in all_place_list:
        place_list.append(place.to_dict())

    return jsonify(place_list), 200


@app_views.route('places/<place_id>',
                 methods=['GET'], strict_slashes=False)
def place_id(place_id):
    """Retrieves a Place object bu his id"""
    obj_place_id = storage.get(Place, place_id)
    if obj_place_id is None:
        abort(404)
    return jsonify(obj_place_id.to_dict())


@app_views.route('places/<place_id>',
                 methods=['DELETE'], strict_slashes=False)
def place_delete(place_id):
    """Delete a Place object by his id"""
    empty = {}
    obj_place_id = storage.get(Place, place_id)
    if obj_place_id is None:
        abort(404)
    storage.delete(obj_place_id)
    storage.save()
    return (jsonify(empty), 200)


@app_views.route('cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def place_create(city_id):
    """Returns the new Place with the status code 201"""
    data = request.get_json()

    obj_place = storage.get(City, city_id)
    if obj_place is None:
        abort(404)

    if data is None:
        return "Not a JSON\n", 400
    if "user_id" not in data:
        return "Missing user_id\n", 400

    """Check if the user exists"""
    user_id = data['user_id']
    obj_user = storage.get(User, user_id)
    if obj_user is None:
        abort(404)
    """Check if 'name' is present in the data"""
    if 'name' not in data:
        return "Missing name\n", 400

    """Create a new Place object"""
    obj_place = Place()
    obj_place.name = data["name"]
    obj_place.city_id = city_id
    obj_place.user_id = user_id
    storage.new(obj_place)
    storage.save()
    return jsonify(obj_place.to_dict()), 201


@app_views.route('places/<place_id>', methods=['PUT'], strict_slashes=False)
def place_update(place_id):
    """Update a Place object by his id"""
    obj_update = storage.get(Place, place_id)
    if obj_update is None:
        abort(404)
    else:
        data = request.get_json()
        if data is None:
            return "Not a JSON\n", 400
        else:
            for key, value in data.items():
                if key not in ["id", "user_id", "city_id",
                               "created_at", "updated_at"]:
                    setattr(obj_update, key, value)
            storage.save()

        return jsonify(obj_update.to_dict()), 200
