#!/usr/bin/python3
""" users """
from models.user import User
from api.v1.views import app_views
from flask import jsonify, request, abort
from models import storage


@app_views.route('/users', strict_slashes=False, methods=['GET', 'POST'])
def user():
    """ users
    """
    if request.method == 'GET':
        data = storage.all(User)
        info = [user.to_dict() for user in data.values()]
        return jsonify(info)

    if request.method == 'POST':
  inf = request.get_json()
if not inf:
abort(400, 'Not a JSON')
if 'email' not in inf:
abort(400, 'Missing email')
if 'password' not in inf:
abort(400, 'Missing password')
user = User(**inf)
storage.new(user)
storage.save()
return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', strict_slashes=False,
methods=['GET', 'DELETE', 'PUT'])
def user_delPutGet(user_id):
""" users
"""
dat = storage.get(User, user_id)

if not dat:
abort(404)

if request.method == 'GET':
return jsonify(dat.to_dict())

if request.method == 'DELETE':
dat.delete()
storage.save()
return jsonify({}), 200

if request.method == 'PUT':
inf = request.get_json()
if not inf:
abort(400, "Not a JSON")

for i, val in inf.items():
if i not in ['id', 'email', 'created_at', 'updated_at']:
setattr(dat, i, val)
dat.save()
storage.save()
return jsonify(dat.to_dict())
