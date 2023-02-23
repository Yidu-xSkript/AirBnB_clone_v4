#!/usr/bin/python3
"""A script that starts a Flask web application"""


from flask import Flask, jsonify, make_response, render_template, url_for
from models import storage
from api.v1.views import app_views
import os
from flask_cors import CORS, cross_origin
from flask import Blueprint
from flasgger import Swagger
from werkzeug.exceptions import HTTPException


app = Flask(__name__)
swagger = Swagger(app)

# global strict slashes
app.url_map.strict_slashes = False

# flask server environmental setup
host = os.getenv('HBNB_API_HOST', '0.0.0.0')
port = os.getenv('HBNB_API_PORT', 5000)

cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
# app_views BluePrint defined in api.v1.views
app.register_blueprint(app_views)

@app.teardown_appcontext
def app_teardown(self):
    """closes DB session"""
    storage.close()


@app.errorhandler(404)
def page_not_found(Error):
    """
    Creates a handler for 404 err that
    returns a JSON-formatted 404 status
    """
    return jsonify({"error": "Not found"}), 404

@app.errorhandler(404)
def handle_404(exception):
    """
    handles 404 errors, in the event that global error handler fails
    """
    code = exception.__str__().split()[0]
    description = exception.description
    message = {'error': description}
    return make_response(jsonify(message), code)


@app.errorhandler(400)
def handle_404(exception):
    """
    handles 400 errros, in the event that global error handler fails
    """
    code = exception.__str__().split()[0]
    description = exception.description
    message = {'error': description}
    return make_response(jsonify(message), code)


@app.errorhandler(Exception)
def global_error_handler(err):
    """
        Global Route to handle All Error Status Codes
    """
    if isinstance(err, HTTPException):
        if type(err).__name__ == 'NotFound':
            err.description = "Not found"
        message = {'error': err.description}
        code = err.code
    else:
        message = {'error': err}
        code = 500
    return make_response(jsonify(message), code)


def setup_global_errors():
    """
    This updates HTTPException Class with custom error function
    """
    for cls in HTTPException.__subclasses__():
        app.register_error_handler(cls, global_error_handler)

if __name__ == "__main__":
    """"""
    # initializes global error handling
    setup_global_errors()
    # start Flask app
    app.run(host=host, port=port)
