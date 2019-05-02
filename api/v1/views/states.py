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
            return 'Not a JSON', 400
        if 'name' not in req_dict.keys():
            return 'Missing name', 400
        new = State(**req_dict)
        storage.new(new)
        storage.save()
        return jsonify(new.to_dict()), 201


@app_views.route('/states/<state_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def state_id_route(state_id):
    state = storage.get("State", state_id)
    if request.method == 'GET':
        if state is None:
            abort(404)
        return jsonify(state.to_dict())
    if request.method == 'DELETE':
        if state is None:
            abort(404)
        storage.delete(state)
        storage.save()
        return jsonify({}), 200
    if request.method == 'PUT':
        if state is None:
            abort(404)
        req_dict = request.get_json(silent=True)
        if req_dict is None:
            return 'Not a JSON', 400
        for key, value in req_dict.items():
            if key != 'id' or key != 'created_at' or key != 'updated_at':
                state.__dict__[key] = value
        storage.save()
        return jsonify(state.to_dict()), 200
