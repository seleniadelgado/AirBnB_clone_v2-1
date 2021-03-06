#!/usr/bin/python3
"""
Handles RESTful API actions for amenities objects
"""
from models import storage
from models.amenity import Amenity
from api.v1.views import app_views
from flask import request, jsonify, abort


@app_views.route('/amenities', strict_slashes=False, methods=['GET', 'POST'])
def amenity_route():
    if request.method == 'GET':
        amenity_list = [amenity.to_dict() for amenity
                        in storage.all("Amenity").values()]
        return jsonify(amenity_list)
    if request.method == 'POST':
        req_dict = request.get_json(silent=True)
        if req_dict is None:
            return jsonify({"error": "Not a JSON"}), 400
        if 'name' not in req_dict.keys():
            return jsonify({"error": "Missing name"}), 400
        new = Amenity(**req_dict)
        new.save()
        return jsonify(new.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def amenity_id_route(amenity_id):
    amenity = storage.get("Amenity", amenity_id)
    if not amenity:
        abort(404)
    if request.method == 'GET':
        return jsonify(amenity.to_dict())
    if request.method == 'DELETE':
        amenity.delete()
        storage.save()
        return jsonify({}), 200
    if request.method == 'PUT':
        req_dict = request.get_json(silent=True)
        if req_dict is None:
            return jsonify({"error": "Not a JSON"}), 400
        for key, value in req_dict.items():
            if key != 'id' and key != 'created_at' and key != 'updated_at':
                setattr(amenity, key, value)
        amenity.save()
        return jsonify(amenity.to_dict())
