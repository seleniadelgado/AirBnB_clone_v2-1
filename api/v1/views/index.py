#!/usr/bin/python3
"""

"""
from api.v1.views import app_views
from flask import Response
import json

@app_views.route('/status', strict_slashes=False) 
def status_route():
    return Response(json.dumps({"status": "OK"}), mimetype='application/json')
