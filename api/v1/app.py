#!/usr/bin/python3
"""
start a Flask web application
"""


import os
from flask import Flask
from flask import Blueprint
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def _close(self):
    """closes app"""
    storage.close()

if __name__ == "__main__":
    if "HBNB_API_HOST" in os.environ:
        hostip = os.environ["HBNB_API_HOST"]
    else:
        hostip = '0.0.0.0'
    if "HBNB_API_PORT" in os.environ:
        portnbr = os.environ["HBNB_API_PORT"]
    else:
        portnbr = 5000
    app.run(hostip, port=portnbr, threaded=True)
