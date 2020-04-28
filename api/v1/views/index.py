#!/usr/bin/python3
""" Create a route /status on the object app_views """
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status')
def status():
    """Create status return"""
    return jsonify({'status': 'OK'})
