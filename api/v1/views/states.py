#!/usr/bin/python3
"""State file for views module"""
from api.v1.views import app_views
from flask import jsonify, request
from models.state import State
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def states():
    """ This method request for states. """
    states = storage.all(State).values()
    return jsonify([item.to_dict() for item in states])


@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def statesById(state_id):
    """ This method filters the state by id. """
    obj = storage.get(State, state_id)
    if obj:
        return jsonify(obj.to_dict())
    return jsonify({"error": "Not found"}), 404


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def statesDelete(state_id):
    """ This method deletes a state by id """
    obj = storage.get(State, state_id)
    if obj:
        storage.delete(obj)
        storage.save()
        return jsonify({}), 200
    return jsonify({"error": "Not found"}), 404


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def statePost():
    """ This method create a new object. """
    try:
        req = request.get_json()
        if 'name' not in req:
            return "Missing name\n", 400
        new_obj = State(name=req['name'])
        storage.new(new_obj)
        storage.save()
        return jsonify(new_obj.to_dict()), 201
    except:
        return "Not a JSON\n", 400


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def statePut(state_id):
    """ This method update an object through http request """
    try:
        req = request.get_json()
        obj = storage.get(State, state_id)
        if obj:
            for key, value in req.items():
                setattr(obj, key, value)
            storage.save()
            return jsonify(obj.to_dict()), 200
        return jsonify({"error": "Not found"}), 404
    except:
        return "Not a JSON\n", 400
