#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = None if not getenv("AUTH_TYPE") else getenv("AUTH_TYPE")


if auth:
    if auth == "basic_auth":
        from api.v1.auth.basic_auth import BasicAuth
        auth = BasicAuth()
    elif auth == "session_auth":
        from api.v1.auth.session_auth import SessionAuth
        auth = SessionAuth()
    elif auth == "session_exp_auth":
        from api.v1.auth.session_exp_auth import SessionExpAuth
        auth = SessionExpAuth()
    elif auth == "session_db_auth":
        from api.v1.auth.session_db_auth import SessionDBAuth
        auth = SessionDBAuth()
    else:
        from api.v1.auth.auth import Auth
        auth = Auth()


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": error.description}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """ Unauthorized handler
    """
    message = error.name
    if error.description == "wrong password":
        message = error.description
    return jsonify({"error": message}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """ Forbidden handler
    """
    return jsonify({"error": error.name}), 403


@app.errorhandler(400)
def forbidden(error) -> str:
    """ Forbidden handler
    """
    return jsonify({"error": error.description}), 400


@app.before_request
def before_request():
    """ Before request handler
    """
    if auth is None:
        return

    excluded_paths = [
                      '/api/v1/status/',
                      '/api/v1/unauthorized/',
                      '/api/v1/forbidden/',
                      '/api/v1/auth_session/login/'
                      ]

    requires_auth = auth.require_auth(request.path, excluded_paths)
    if not requires_auth:
        return

    current_user = auth.current_user(request)

    authorization_header = auth.authorization_header(request)
    session_cookie = auth.session_cookie(request)
    if not authorization_header and not session_cookie:
        abort(401)

    current_user = auth.current_user(request)
    if not current_user:
        abort(403)

    request.current_user = current_user


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
