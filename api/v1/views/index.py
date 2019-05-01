#!/usr/bin/python3
"""

"""
from api.v1.views import app_views
from flask import jsonify
import json
from models import storage

stat_dict = {"amenities": storage.count("amenities"),
             "cities": storage.count("cities"),
             "places": storage.count("places"),
             "reviews": storage.count("reviews"),
             "states": storage.count("states"),
             "users": storage.count("users")}

@app_views.route('/status', strict_slashes=False)
def status_route():
    return jsonify({"status": "OK"})

@app_views.route('/stats', strict_slashes=False)
def stats_route():
    return jsonify(stat_dict)

