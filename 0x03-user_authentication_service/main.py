#!/usr/bin/env python3
""" End-to-end integration test
"""

import requests
import json


BASE_URL = 'http://0.0.0.0:5000'


def register_user(email: str, password: str) -> None:
    """ Tests POST /users endpoint
    """
    payload = {'email': email, 'password': password}
    actual_response = requests.post(f'{BASE_URL}/users', data=payload)
    expected_response = {'email': email, 'message': 'user created'}

    assert actual_response.status_code == 200
    assert actual_response.json() == expected_response

    # On failure
    actual_response = requests.post(f'{BASE_URL}/users', data=payload)
    expected_response = {'message': 'email already registered'}

    assert actual_response.status_code == 400
    assert actual_response.json() == expected_response


def log_in_wrong_password(email: str, password: str) -> None:
    """ Test POST /sessions endpoint with wrong credentials
    """
    payload = {'email': email, 'password': password}
    actual_response = requests.post(f'{BASE_URL}/sessions', data=payload)

    assert actual_response.status_code == 401


def log_in(email: str, password: str) -> str:
    """ Test POST /sessions endpoint with wrong credentials
    """
    payload = {'email': email, 'password': password}
    actual_response = requests.post(f'{BASE_URL}/sessions', data=payload)
    expected_response = {'email': email, 'message': 'logged in'}

    assert actual_response.status_code == 200
    assert actual_response.json() == expected_response

    return actual_response.cookies.get('session_id')


def profile_unlogged() -> None:
    """ Test GET /profile endpoint without authentication
    """
    response = requests.get(f'{BASE_URL}/profile')
    assert response.status_code == 403


def profile_logged(session_id: str) -> None:
    """ Test GET /profile endpoint with authentication
    """
    cookies = {'session_id': session_id}
    actual_response = requests.get(f'{BASE_URL}/profile', cookies=cookies)
    expected_response = {'email': EMAIL}

    assert actual_response.status_code == 200
    assert actual_response.json() == expected_response


def log_out(session_id: str) -> None:
    """ Logout a user
    """
    cookies = {'session_id': session_id}
    response = requests.delete(f'{BASE_URL}/sessions', cookies=cookies)

    assert response.status_code == 200
    assert response.json() == {'message': 'Bienvenue'}

    response = requests.delete(f'{BASE_URL}/sessions', cookies=cookies)

    assert response.status_code == 403


def reset_password_token(email: str) -> str:
    """ Get reset password token
    """
    payload = {'email': email}
    actual_response = requests.post(f'{BASE_URL}/reset_password',
                                    data=payload)
    reset_token = actual_response.json().get('reset_token')
    expected_response = {
                         'email': email,
                         'reset_token': reset_token
                         }

    assert actual_response.status_code == 200
    assert actual_response.json() == expected_response

    payload = {'email': 'fake@email.com'}
    actual_response = requests.post(f'{BASE_URL}/reset_password', data=payload)

    assert actual_response.status_code == 403

    return reset_token


def update_password(email: str, reset_token: str, new_password: str) -> None:
    """ Update a user's password
    """
    payload = {
               'email': email,
               'reset_token': reset_token,
               'new_password': new_password
               }

    actual_response = requests.put(f'{BASE_URL}/reset_password', data=payload)
    assert actual_response.status_code == 200

    actual_response = requests.put(f'{BASE_URL}/reset_password', data=payload)
    assert actual_response.status_code == 403


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    log_in(EMAIL, PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
