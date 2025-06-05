# User authentication service
  - How to declare API routes in a Flask app
  - How to get and set cookies
  - How to retrieve request form data
  - How to return various HTTP status codes

# Simple API
  Simple HTTP API with a session based authentication service for playing with User model

## Files
  - `app.py`: entry point of the API
  - `auth.py`: session authentication service
  - `db.py`: database storage engine
  - `user.py`: user model
  - `main.py`: end-to-end integration test

## Setup
  ```bash
    python3 -m venv .env
    source .env/bin/activate
    pip3 install -r requirements.txt
  ```

## Run
  ```bash
  API_HOST=0.0.0.0 API_PORT=5000 python3 -m app
  ```

## Routes
  - `GET /`: returns `{'message': 'Bienvenue'}`
  - `POST /users`: creates a new user (JSON parameters: `email`, `password`)
  - `POST /sessions`: login a user (JSON parameters: `email`, `password`) and returns the session id as a cookie(session_id)
  - `DELETE /sessions`: logout a user(expected request cookie: `session_id`)
  - `GET /profile`: returns a user profile if exists(expected request cookie: `session_id`)
  - `POST /reset_password`: generates and returns a reset password token (JSON parameters: `email`)
  - `PUT /reset_password`: updates a user's password (expected request cookies: `email`, `reset_token`, and `new_password`)
