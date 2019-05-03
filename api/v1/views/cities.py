#!/usr/bin/python3
"""
Handles RESTful API actions for city objects
"""
from models import storage
from models.city import City
from api.v1.views import app_views
from flask import request, jsonify, abort


@app_views.route('/cities', strict_slashes=False, methods=['GET', 'POST'])
def city_route():
    if request.method == 'GET':
        city_list = [city.to_dict() for city in storage.all("City").values()]
        return jsonify(city_list)
        if request.method == 'POST':
            req_dict = request.get_json(silent=True)
            if req_dict is None:
                return jsonify({"error": "Not a JSON"}), 400
            if 'name' not in req_dict.keys():
                return jsonify({"error": "Missing name"}), 400
            new = city(**req_dict)
            new.save()
            return jsonify(new.to_dict()), 201


@app_views.route('/cities/<city_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def city_id_route(city_id):
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(city.to_dict())
    if request.method == 'DELETE':
        city.delete()
        storage.save()
        return jsonify({}), 200
    if request.method == 'PUT':
        req_dict = request.get_json(silent=True)
        if req_dict is None:
            return jsonify({"error": "Not a JSON"}), 400
        for key, value in req_dict.items():
            if key != 'id' and key != 'created_at' and \
                    key != 'updated_at' and key != 'state_id':
                setattr(city, key, value)
            city.save()
            return jsonify(city.to_dict())


@app_views.route('/states/<state_id>/cities', strict_slashes=False,
                 methods=['GET', 'POST'])
def city_state_id_route(state_id):
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    if request.method == 'GET':
        city_list = [city.to_dict() for city in storage.all("City").values()
                     if city.state_id == state_id]
        return jsonify(city_list)
