#!/usr/bin/python3
'''Contains the places_amenities view for the API.'''
from flask import jsonify, request
from werkzeug.exceptions import NotFound, MethodNotAllowed

from api.v1.views import app_views
from models import storage, storage_t
from models.amenity import Amenity
from models.place import Place


@app_views.route('/places/<place_id>/amenities', methods=['GET'])
@app_views.route(
    '/places/<place_id>/amenities/<amenity_id>',
    methods=['DELETE', 'POST']
)
def handle_places_amenities(place_id=None, amenity_id=None):
    '''The method handler for the places endpoint.'''
    handlers = {
        'GET': get_place_amenities,
        'DELETE': remove_place_amenity,
        'POST': add_place_amenity
    }
    if request.method in handlers:
        return handlers[request.method](place_id, amenity_id)
    else:
        raise MethodNotAllowed(list(handlers.keys()))


def get_place_amenities(place_id=None, amenity_id=None):
    '''Gets the amenities of a place with the given id.'''
    place = storage.get(Place, place_id)
    if place:
        all_amenities = [amenity.to_dict() for amenity in place.amenities]
        return jsonify(all_amenities)
    raise NotFound()


def remove_place_amenity(place_id=None, amenity_id=None):
    '''Removes an amenity with a given id from a place with a given id.'''
    place = storage.get(Place, place_id)
    if not place:
        raise NotFound()
    
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        raise NotFound()
    
    if amenity not in place.amenities:
        raise NotFound()
    
    if storage_t == 'db':
        place.amenities.remove(amenity)
    else:
        place.amenity_ids.remove(amenity_id)
    
    place.save()
    return jsonify({}), 200


def add_place_amenity(place_id=None, amenity_id=None):
    '''Adds an amenity with a given id to a place with a given id.'''
    place = storage.get(Place, place_id)
    if not place:
        raise NotFound()
    
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        raise NotFound()
    
    if storage_t == 'db':
        if amenity in place.amenities:
            return jsonify(amenity.to_dict()), 200
        place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return jsonify(amenity.to_dict()), 200
        place.amenity_ids.append(amenity_id)
    
    place.save()
    return jsonify(amenity.to_dict()), 201

