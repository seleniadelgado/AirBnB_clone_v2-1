#!/usr/bin/python3
"""

"""
from api.v1.views import app_views
from flask import jsonify
import json


@app_views.route('/status', strict_slashes=False)
def status_route():
    return jsonify({"status": "OK"})
