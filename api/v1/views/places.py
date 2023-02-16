#!/usr/bin/python3
"""
Create a new view for Places objects that handles
all default RESTful API actions
"""
from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.city import City
from models.place import Place


@app_views.route('/places/<place_id>', methods=['GET'], strict_slashes=False)
def get_place(place_id=None):
    """List retrieval of all Place objects for a city"""
    cities_all = storage.all('City', city_id)
    if city_all is None:
        abort(404)
    placesLIST = []
    places_all = storage.all('Place').values()
    city_p = [p.to_dict() for p in places_all if p.city_id == city_id]
    return jsonify(city_p)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def place_retrieval(place_id=None):
    """Retrieval of Place objects with linked place ids"""
    place = storage.get('Place', place_id)
    if place is None:  # if place_id is not linked to any place obj
        abort(404)  # then, raise 404 error
    else:
        return jsonify(place.to_dict()), 200


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id=None):
    """Deletes a Place object"""
    objects = storage.get('Place', place_id)
    if objects is None:
        abort(404)  # if the user_id is not linked to any User object
    storage.delete(objects)
    storage.save()
    return jsonify({}), 200  # returns an empty dict with status code 200

