#!/usr/bin/python3
"""

"""
from api.v1.views import app_views
from flask import jsonify
import json
from models import storage


stat_dict = {"amenities": storage.count("Amenity"),
             "cities": storage.count("City"),
             "places": storage.count("Place"),
             "reviews": storage.count("Review"),
             "states": storage.count("State"),
             "users": storage.count("User")}


@app_views.route('/status', strict_slashes=False)
def status_route():
    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def stats_route():
    return jsonify(stat_dict)
