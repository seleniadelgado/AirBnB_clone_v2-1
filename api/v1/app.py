#!/usr/bin/python3
"""
start a Flask web application
"""


import os
from flask import Flask
from flask import Blueprint
from models import storage
from api.v1.views import app_views
from flask import jsonify
app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def _close(self):
    """closes app"""
    storage.close()

@app.errorhandler(404)
def  page_not_found(e):
    response = jsonify({"error": "Not found"})
    response.status_code = 404
    return response
    
if __name__ == "__main__":
    if "HBNB_API_HOST" in os.environ:
        hostip = os.environ["HBNB_API_HOST"]
    else:
        hostip = '0.0.0.0'
    if "HBNB_API_PORT" in os.environ:
        portnbr = os.environ["HBNB_API_PORT"]
    else:
        portnbr = 5000
    app.run(host=hostip, port=portnbr, threaded=True)