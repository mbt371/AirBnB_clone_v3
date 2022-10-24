#!/usr/bin/python3
"""Amenity file for views module"""
from api.v1.views import app_views
from flask import jsonify, request
from models.amenity import Amenity
from models import storage


@app_views.route('/amenities', methods=['GET'], strict_slashes=False)
def amenities():
    """ This method request for amenities. """
    amenities = storage.all(Amenity).values()
    return jsonify([item.to_dict() for item in amenities])


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def amenities_id(amenity_id):
    """ This method filters the amenities by id. """
    amenities = storage.all(Amenity).values()
    obj = [item for item in amenities if item.id == amenity_id]
    if obj:
        return jsonify(obj[0].to_dict())
    return jsonify({"error": "Not found"}), 404


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def amenitiesDelete(amenity_id):
    """ This method deletes a amenity by id """
    obj = storage.get(Amenity, amenity_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200
    return jsonify({"error": "Not found"}), 404


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def amenitiesPost():
    """ This method create a new object. """
    try:
        req = request.get_json()
        if 'name' not in req:
            return "Missing name\n", 400
        new_obj = Amenity(name=req['name'])
        storage.new(new_obj)
        storage.save()
        return jsonify(new_obj.to_dict()), 201
    except:
        return "Not a JSON\n", 400


@app_views.route('/amenities/<amenity_id>',
                 methods=['PUT'], strict_slashes=False)
def amenitiesPut(amenity_id):
    """ This method update an object through http request """
    try:
        req = request.get_json()
        obj = storage.get(Amenity, amenity_id)
        if obj:
            for key, value in req.items():
                setattr(obj, key, value)
            storage.save()
            return jsonify(obj.to_dict()), 200
        return jsonify({"error": "Not found"}), 404
    except:
        return "Not a JSON\n", 400
