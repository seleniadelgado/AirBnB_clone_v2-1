#!/usr/bin/python3
"""
Handles RESTful API actions for State objects
"""
from models import storage
from models.state import State
from api.v1.views import app_views
from flask import request, jsonify, abort


@app_views.route('/states', strict_slashes=False, methods=['GET', 'POST'])
def state_route():
    if request.method == 'GET':
        state_list = [state.to_dict() for state
                      in storage.all("State").values()]
        return jsonify(state_list)
    if request.method == 'POST':
        req_dict = request.get_json(silent=True)
        if req_dict is None:
            return jsonify({"error": "Not a JSON"}), 400
        if 'name' not in req_dict.keys():
            return jsonify({"error": "Missing name"}), 400
        new = State(**req_dict)
        new.save()
        return jsonify(new.to_dict()), 201


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def state_id_route(state_id):
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(state.to_dict())
    if request.method == 'DELETE':
        state.delete()
        storage.save()
        return jsonify({}), 200
    if request.method == 'PUT':
        req_dict = request.get_json(silent=True)
        if req_dict is None:
            return jsonify({"error": "Not a JSON"}), 400
        for key, value in req_dict.items():
            if key != 'id' and key != 'created_at' and key != 'updated_at':
                setattr(state, key, value)
        state.save()
        return jsonify(state.to_dict())
