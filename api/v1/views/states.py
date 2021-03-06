#!/usr/bin/python3
""" module state viwes"""
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/states/', methods=['GET'])
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def all_states(state_id=None):
    '''Returns all states object in json format'''
    json_list = []
    try:
        if state_id is None:
            for v in storage.all('State').values():
                json_list.append(v.to_dict())
        else:
            json_list = storage.get('State', state_id).to_dict()
        return jsonify(json_list)
    except Exception:
        abort(404)


@app_views.route('/states/', methods=['POST'], strict_slashes=False)
def create_state():
    '''Creates an instance of State and save it to storage'''
    form = request.get_json(force=True)
    if 'name' not in request.json:
        return jsonify({"error": "Missing name"}), 400
    new_state = State(**form)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_state(state_id):
    '''Deletes a state object'''
    state_obj = storage.get('State', state_id)
    if state_obj is None:
        abort(404)
    else:
        storage.delete(state_obj)
        storage.save()
    return jsonify({})


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    '''Updates State object attribute'''
    state_obj = storage.get('State', state_id)
    if state_obj is None:
        abort(404)
    form = request.get_json(force=True)
    attrib_update(state_obj, **form)
    state_obj.save()
    return jsonify(state_obj.to_dict()), 200
