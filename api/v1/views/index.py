#!/usr/bin/python3
"""Route of the index"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """Returns the status of the API"""
    return jsonify(status="OK")


@app_views.route('/stats')
def stats():
    """Retrieves the number of each objects by type"""
    objects_count = {
        "amenities": storage.count('Amenity'),
        "cities": storage.count('City'),
        "places": storage.count('Place'),
        "reviews": storage.count('Review'),
        "states": storage.count('State'),
        "users": storage.count('User')
    }
    return jsonify(objects_count)
