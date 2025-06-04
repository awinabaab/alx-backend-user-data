#!/usr/bin/env python3
""" Basic Flask app
"""

from flask import (
    Flask, jsonify, request, abort, make_response, redirect, url_for
)
from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/", strict_slashes=False)
def index() -> str:
    """ Index route
    """
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=['POST'], strict_slashes=False)
def users() -> str:
    """ Registers a new user
    """
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        user = AUTH.register_user(email, password)
        return jsonify({"email": email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=['POST'], strict_slashes=False)
def login():
    """ Login a user
    """
    email = request.form.get("email")
    password = request.form.get("password")

    is_valid_login = AUTH.valid_login(email, password)
    if not is_valid_login:
        abort(401)

    session_id = AUTH.create_session(email)
    response = make_response(jsonify({"email": email, "message": "logged in"}))
    response.set_cookie("session_id", session_id)

    return response


@app.route("/sessions", methods=['DELETE'], strict_slashes=False)
def logout() -> str:
    """ Logout a user
    """
    session_id = request.cookies.get("session_id")

    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)

    AUTH.destroy_session(user.id)

    return redirect(url_for("index"))


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> str:
    """ Finds and returns a user profile
    """
    session_id = request.cookies.get("session_id")

    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)

    return jsonify({"email": user.email})


@app.route("/reset_password", methods=['POST'], strict_slashes=False)
def get_reset_password_token() -> str:
    """ Generates a reset password token
    """
    email = request.form.get("email")

    try:
        reset_token = AUTH.get_reset_password_token(email)
        return jsonify({"email": email, "reset_token": reset_token})
    except ValueError as e:
        abort(403)


@app.route("/reset_password", methods=['PUT'], strict_slashes=False)
def update_password() -> str:
    """ Updates the password of a user
    """
    email = request.form.get("email")
    reset_token = request.form.get("reset_token")
    new_password = request.form.get("new_password")

    try:
        AUTH.update_password(reset_token, new_password)
        return jsonify({"email": email, "message": "Password updated"})
    except ValueError as e:
        abort(403)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
