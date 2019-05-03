#!/usr/bin/python3
"""
Handles RESTful API actions for place objects
"""
from models import storage
from models.place import Place
from api.v1.views import app_views
from flask import request, jsonify, abort


@app_views.route('/places/<place_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def place_id_route(place_id):
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(place.to_dict())
    if request.method == 'DELETE':
        place.delete()
        storage.save()
        return jsonify({}), 200
    if request.method == 'PUT':
        req_dict = request.get_json(silent=True)
        if req_dict is None:
            return jsonify({"error": "Not a JSON"}), 400
        for key, value in req_dict.items():
            if key != 'id' and key != 'created_at' and \
                    key != 'updated_at' and key != 'user_id' and \
                    key != 'city_id':
                setattr(place, key, value)
            place.save()
            return jsonify(place.to_dict())


@app_views.route('/cities/<city_id>/places', strict_slashes=False,
                 methods=['GET', 'POST'])
def place_state_id_route(state_id):
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    if request.method == 'GET':
        place_list = [place.to_dict() for place in
                      storage.all("Place").values()
                      if place.city_id == city_id]
        return jsonify(place_list)
    if request.method == 'POST':
        req_dict = request.get_json(silent=True)
        if req_dict is None:
            return 'Not a JSON', 400
        if 'name' not in req_dict.keys():
            return 'Missing name', 400
        if 'user_id' not in req_dict.keys():
            return 'Missing user_id', 400
        user = storage.get("User", user_id)
        if user is None:
            abort(404)
        new = Place(**req_dict)
        new.save()
        return jsonify(new.to_dict()), 201
