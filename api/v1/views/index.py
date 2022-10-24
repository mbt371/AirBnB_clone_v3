#!/usr/bin/python3
"""This script defines a route status"""
from api.v1.views import app_views
from flask import jsonify
from models import storage
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.amenity import Amenity
from models.review import Review


@app_views.route('/status')
def status():
    """Request status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    """Count all classes"""
    dicc = {}
    list_items = {
        'states': State,
        'cities': City,
        'users': User,
        'places': Place,
        'amenities': Amenity,
        'reviews': Review
    }

    for key, value in list_items.items():
        dicc[key] = storage.count(value)
    return jsonify(dicc)
