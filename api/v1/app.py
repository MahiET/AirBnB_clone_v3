#!/usr/bin/python3

from flask import Flask, jsonify
from models import storage
import os
from flask_cors import CORS
from api.v1.views import app_views

app = Flask(__name__)
''' The Flask web application instance'''
app_host = os.getenv('HBNB_API_HOST', '0.0.0.0')
app_port = int(os.getenv('HBNB_API_PORT', '5000'))
app.url_map.strict_slashes = False
app.register_blueprint(app_views)
CORS(app, resources={'/*': {'origins': app_host}})


@app.teardown_appcontext
def teardown_flask(exception):
    ''' The Flask app/request context end event listener '''
    # print(exception)
    storage.close()


@app.errorhandler(404)
def error_404(error):
    '''
    a handler for 404 errors that returns a
    JSON-formatted 404 status code response
    '''
    return (jsonify({"error": "Not found"}), 404)

@app.errorhandler(400)
def error_400(error):
    '''Handles the 400 HTTP error code.'''
    msg = 'Bad request'
    if isinstance(error, Exception) and hasattr(error, 'description'):
        msg = error.description
    return jsonify(error=msg), 400


if __name__ == "__main__":
    hosts = os.getenv("HBNB_API_HOST", default='0.0.0.0')
    ports = int(os.getenv("HBNB_API_PORT", default='5000'))
    app.run(host=hosts, port=ports, threaded=True)
