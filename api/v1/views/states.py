#!/usr/bin/python3
""" module state viwes"""


from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State
app.url_map.strict_slashes = False


@app_views.route('/states/',methods=['GET'])
def all_states():
    """Retrieves the list of all State objects"""
    all_states = []
    for state in storage.all('State').values():
        all_states.append(state.to_dict())
    return jsonify(all_states)


@app_views.route('/states/<state_id>', method=['GET'])
def retrieve_state(state_id):
    """If the state_id is not linked to any State object, raise a 404 error """
    try:
        state = jsonify(storage.get('State', state_id).to_dict())
        return state
    except:
        abort(404)


@app_views.route('/states/<state_id>', method=['DELETE'])
def delete_state(state_id):
    """delete state object"""
    state_obj = storage.get('State', state_id)
    if state_obj is None:
        abort(404)
    else:
        storage.delete(state_obj)
        storage.save()
    return jsonify({})


@app_views.route('/states/', methods=['POST'])
def create_state():
    """Create an stance of state and save in to storage"""
    form = request.get_json(force=True)
    if 'name' not in request.json:
        return jsonify({"error: Missing name"}), 400
    state_class = models.classes['State']
    new_state = state_class()
    attrib_update(new_state, **form)
    new_state.save()
    return jsonify(new_state.to_dict()), 201


@app_niews.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """ Updates State object attribite """
    state_obj = storage.get('State', state_id)
    if state_obj is None:
            abort(404)
    form = request.get_json(force=True)
    attrib_update(state_obj), **form)
    state_obj.save()
    return jsonify(state_obj.to_dict()), 200