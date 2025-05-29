#!/usr/bin/env python3
""" Module of SessionAuth views
"""
from flask import jsonify, abort, request, make_response
from models.user import User
from api.v1.views import app_views
import os


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> str:
    """ GET /api/v1/auth_session/login
    Return:
      - Handles authentication for a session
    """
    user_email = request.form.get('email')
    if user_email is None or len(user_email) == 0:
        abort(400, "email is missing")

    user_pwd = request.form.get('password')
    if user_pwd is None or len(user_pwd) == 0:
        abort(400, "password is missing")

    users = User.search({"email": user_email})
    if not users or len(users) == 0:
        abort(404, "no user found for this email")

    user = users[0]
    is_valid_password = user.is_valid_password(user_pwd)
    if not is_valid_password:
        abort(401, "wrong password")

    from api.v1.app import auth

    SESSION_NAME = os.getenv("SESSION_NAME")
    session_id = auth.create_session(user.id)
    response = make_response(jsonify(user.to_json()))
    response.set_cookie(SESSION_NAME, session_id)

    return response


@app_views.route('/auth_session/logout',
                 methods=['DELETE'],
                 strict_slashes=False)
def logout() -> str:
    """ GET /api/v1/auth_session/login
    Return:
      - Handles logout for a session
    """
    from api.v1.app import auth

    logged_out = auth.destroy_session(request)
    print(logged_out)
    if not logged_out:
        abort(404)

    return jsonify({}), 200
