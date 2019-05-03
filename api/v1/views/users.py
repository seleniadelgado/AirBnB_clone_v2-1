#!/usr/bin/python3
"""
Handles RESTful API actions for User objects
"""
from models import storage
from models.user import User
from api.v1.views import app_views
from flask import request, jsonify, abort


@app_views.route('/users', strict_slashes=False, methods=['GET', 'POST'])
def user_route():
    if request.method == 'GET':
        user_list = [user.to_dict() for user
                     in storage.all("User").values()]
        return jsonify(user_list)

    if request.method == 'POST':
        req_dict = request.get_json(silent=True)
        if req_dict is None:
            return jsonify({"error": "Not a JSON"}), 400
        if 'email' not in req_dict.keys():
            return jsonify({"error": "Missing email"}), 400
        if 'password' not in req_dict.keys():
            return jsonify({"error": "Missing password"}), 400
        new = User(**req_dict)
        new.save()
        return jsonify(new.to_dict()), 201


@app_views.route('/users/<user_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def user_id_route(user_id):
    user = storage.get("User", user_id)
    if not user:
        abort(404)
    if request.method == 'GET':
        return jsonify(user.to_dict())

    if request.method == 'DELETE':
        user.delete()
        storage.save()
        return jsonify({}), 200

    if request.method == 'PUT':
        req_dict = request.get_json(silent=True)
        if req_dict is None:
            return jsonify({"error": "Not a JSON"}), 400
        for key, value in req_dict.items():
            if key != 'id' and key != 'created_at' and key != 'updated_at':
                setattr(user, key, value)
        user.save()
        return jsonify(user.to_dict())
