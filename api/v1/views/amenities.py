#!/usr/bin/python3
"""Amenity objects that handles all default RESTFul API actions"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models import storage
from models.state import State
from models.amenity import Amenity


@app_views.route('/amenities', strict_slashes=False)
def amenities():
    """List all Amenity object into a valid JSON"""
    list_obj = []
    dict_storage = storage.all(Amenity)

    for key, value in dict_storage.items():
        list_obj.append(value.to_dict())
    return jsonify(list_obj)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def amenities_id(amenity_id):
    """Retrieves a Amenity object by his id"""
    obj_state_id = storage.get(Amenity, amenity_id)
    if obj_state_id is None:
        abort(404)
    return jsonify(obj_state_id.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def amenity_delete(amenity_id):
    """Delete a Amenity object by his id"""
    empty = {}
    obj_state_id = storage.get(Amenity, amenity_id)
    if obj_state_id is None:
        abort(404)
    storage.delete(obj_state_id)
    storage.save()
    return (jsonify(empty), 200)


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def amenities_create():
    """Returns the new Amenity with the status code 201"""
    data = request.get_json()
    if data is None:
        return "Not a JSON\n", 400
    elif "name" not in data:
        return "Missing name\n", 400
    else:
        obj = Amenity()
        obj.name = data["name"]
        storage.new(obj)
        storage.save()
        return jsonify(obj.to_dict()), 201


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def amenities_update(amenity_id):
    """Update a Amenity object by his id"""
    obj_update = storage.get(Amenity, amenity_id)
    if obj_update is None:
        abort(404)
    else:
        data = request.get_json()
        if data is None:
            return "Not a JSON\n", 400
        else:
            for key, value in data.items():
                if key not in ["id", "created_at", "updated_at"]:
                    setattr(obj_update, key, value)
            storage.save()

        return jsonify(obj_update.to_dict()), 200
