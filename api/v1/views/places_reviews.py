#!/usr/bin/python3
"""Reviews file for views module"""
from api.v1.views import app_views
from flask import jsonify, request
from models.place import Place
from models.review import Review
from models.user import User
from models import storage


@app_views.route('/places/<place_id>/reviews',
                 methods=['GET'], strict_slashes=False)
def reviews(place_id):
    """ This method request for reviews. """
    place_nedded = storage.get(Place, place_id)
    if place_nedded:
        return jsonify([item.to_dict() for item in place_nedded.reviews])
    return jsonify({"error": "Not found"}), 404


@app_views.route('/reviews/<review_id>',
                 methods=['GET'], strict_slashes=False)
def reviews_id(review_id):
    """ This method filters the reviews by id. """
    obj = storage.get(Review, review_id)
    if obj:
        return jsonify(obj.to_dict())
    return jsonify({"error": "Not found"}), 404


@app_views.route('/reviews/<review_id>',
                 methods=['DELETE'], strict_slashes=False)
def reviewDelete(review_id):
    """ This method deletes a review by id """
    obj = storage.get(Review, review_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200
    return jsonify({"error": "Not found"}), 404


@app_views.route('/places/<place_id>/reviews',
                 methods=['POST'], strict_slashes=False)
def reviewsPost(place_id):
    """ This method create a new object. """
    obj = storage.get(Place, place_id)
    if not obj:
        return jsonify({"error": "Not found"}), 404
    try:
        req = request.get_json()
        if 'user_id' not in req:
            return "Missing user_id", 400
        idUser = storage.get(User, req["user_id"])
        if not idUser:
            return jsonify({"error": "Not found"}), 404
        if 'text' not in req:
            return "Missing text", 400
        req["place_id"] = place_id
        new_obj = Review(**req)
        storage.new(new_obj)
        storage.save()
        return jsonify(new_obj.to_dict()), 201
    except:
        return "Not a JSON\n", 400


@app_views.route('/reviews/<review_id>',
                 methods=['PUT'], strict_slashes=False)
def reviewsPut(review_id):
    """ This method update an object through http request """
    try:
        req = request.get_json()
        obj = storage.get(Review, review_id)
        if obj:
            for key, value in req.items():
                setattr(obj, key, value)
            storage.save()
            return jsonify(obj.to_dict()), 200
        return jsonify({"error": "Not found"}), 404
    except:
        return "Not a JSON\n", 400
