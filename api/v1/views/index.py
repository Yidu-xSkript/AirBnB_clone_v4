#!/usr/bin/python3
"""Index Route file for a flask web app"""


from api.v1.views import app_views
from flask import Flask, jsonify

@app_views.route('/status', methods=['GET'], strict_slashes=False)
def status():
    """Returns the JSON status"""
    return jsonify({"status": "OK"})
