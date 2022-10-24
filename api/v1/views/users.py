#!/usr/bin/python3
"""User file for views module"""
from api.v1.views import app_views
from flask import jsonify, request
from models.user import User
from models import storage


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def users():
    """ This method request for users. """
    users = storage.all(User).values()
    return jsonify([item.to_dict() for item in users])


@app_views.route('/users/<user_id>',
                 methods=['GET'], strict_slashes=False)
def users_id(user_id):
    """ This method filters the users by id. """
    users = storage.all(User).values()
    obj = [item for item in users if item.id == user_id]
    if obj:
        return jsonify(obj[0].to_dict())
    return jsonify({"error": "Not found"}), 404


@app_views.route('/users/<user_id>',
                 methods=['DELETE'], strict_slashes=False)
def usersDelete(user_id):
    """ This method deletes a amenity by id """
    obj = storage.get(User, user_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200
    return jsonify({"error": "Not found"}), 404


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def usersPost():
    """ This method create a new object. """
    try:
        req = request.get_json()
        if 'email' not in req:
            return "Missing email\n", 400
        if 'password' not in req:
            return "Missing password\n", 400
        new_obj = User()
        for key, value in req.items():
            setattr(new_obj, key, value)
        storage.new(new_obj)
        storage.save()
        return jsonify(new_obj.to_dict()), 201
    except:
        return "Not a JSON\n", 400


@app_views.route('/users/<user_id>',
                 methods=['PUT'], strict_slashes=False)
def usersPut(user_id):
    """ This method update an object through http request """
    try:
        req = request.get_json()
        obj = storage.get(User, user_id)
        if obj:
            for key, value in req.items():
                setattr(obj, key, value)
            storage.save()
            return jsonify(obj.to_dict()), 200
        return jsonify({"error": "Not found"}), 404
    except:
        return "Not a JSON\n", 400
