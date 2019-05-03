#!/usr/bin/python3
"""
Handles RESTful API actions for review objects
"""
from models import storage
from models.review import Review
from api.v1.views import app_views
from flask import request, jsonify, abort


@app_views.route('/reviews/<review_id>', strict_slashes=False,
                 methods=['GET', 'DELETE', 'PUT'])
def review_id_route(review_id):
    review = storage.get("Review", review_id)
    if review is None:
        abort(404)
    if request.method == 'GET':
        return jsonify(review.to_dict())
    if request.method == 'DELETE':
        review.delete()
        storage.save()
        return jsonify({}), 200
    if request.method == 'PUT':
        req_dict = request.get_json(silent=True)
        if req_dict is None:
            return jsonify({"error": "Not a JSON"}), 400
        for key, value in req_dict.items():
            if key != 'id' and key != 'created_at' and \
                    key != 'updated_at' and key != 'user_id' and \
                    key != 'place_id':
                setattr(review, key, value)
        review.save()
        return jsonify(review.to_dict())


@app_views.route('/cities/<city_id>/reviews', strict_slashes=False,
                 methods=['GET', 'POST'])
def review_city_id(city_id):
    place = storage.get("Place", city_id)
    if place is None:
        abort(404)
    if request.method == 'GET':
        review_list = [review.to_dict() for review in
                       storage.all("Review").values()
                       if review.place_id == place_id]
        return jsonify(review_list)
    if request.method == 'POST':
        req_dict = request.get_json(silent=True)
        if req_dict is None:
            return 'Not a JSON', 400
        if 'name' not in req_dict.keys():
            return 'Missing name', 400
        if 'user_id' not in req_dict.keys():
            return 'Missing user_id', 400
        if 'text' not in req_dict.keys():
            return 'Missing text', 400
        user = storage.get("User", user_id)
        if user is None:
            abort(404)
        new = review(**req_dict)
        new.save()
        return jsonify(new.to_dict()), 201
