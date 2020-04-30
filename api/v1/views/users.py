 #!/usr/bin/python3
""" module state viwes"""
from flask import Flask, jsonify, abort, request
from api.v1.views import app_views
from models import storage
from models.state import State


@app_views.route('/users/', methods=['GET'])
@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def all_users(user_id=None):
    '''Returns all users object in json format'''
    json_list = []
    try:
        if user_id is None:
            for v in storage.all('User').values():
                json_list.append(v.to_dict())
        else:
            json_list = storage.get('State', state_id).to_dict()
        return jsonify(json_list)
    except Exception:
        abort(404)

@app_views.route('/users/', methods=['POST'], strict_slashes=False)
def create_users():
    '''Creates an instance of user and save it to storage'''
    try:
        form = request.get_json()
    except Exception:
        abort(404, "Not a JSON")
    if form:
        if 'email' not in form:
            return jsonify({"error": "Missing email"}), 400
        elif 'password' not in form:
            return jsonify({"erro": "Missing password"}), 400
        new_user = User(**form)
        new_user.save()
        return jsonify(new_user.to_dict()), 201
    else:
        abort(404, "Not a JSON")

@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_user(state_id):
    '''Deletes a user object'''
    user_obj = storage.get('User', user_id)
    if user_obj is None:
        abort(404)
    else:
        storage.delete(user_obj)
        storage.save()
    return jsonify({})


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    '''Updates user object attribute'''
    state_obj = storage.get('User', user_id)
    if user_obj is None:
        abort(404)
    form = request.get_json(force=True)
    attrib_update(user_obj, **form)
    user_obj.save()
    return jsonify(user_obj.to_dict()), 200
