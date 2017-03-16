from flask import (
    render_template,
    request, session,
    flash, url_for,
    redirect, make_response,
    after_this_request, g,
    abort, Response, Blueprint
)
from api.services.auth import AuthService
from api.exceptions.auth import AuthError
from api.exceptions.user import UserError
from api.helpers import jsonize


controller = ctrlr = Blueprint('auth', __name__)
auth_service = AuthService()


@ctrlr.route("/auth/", methods=['POST'])
@jsonize
def auth_authenticate():
    """
    Authenticates and returns an `authorization_token` for the current user.

    ---
    tags:
      - Auth
    parameters:
      - name: body
        in: body
        description: User credentials JSON.
        schema:
          $ref: '#/definitions/AuthData'
        required: true
    responses:
      201:
        description: '`authorization_token` created successfully.'
        schema:
          $ref: '#/definitions/AuthToken'
      400:
        description: Request is invalid.
      401:
        description: Provided credentials are invalid.

    definitions:
      - schema:
          id: AuthData
          required:
            - email
            - password
          properties:
            email:
              type: string
              description: user's email address
            password:
              type: string
              description: user's password
      - schema:
          id: AuthToken
          required:
            - authorization_token
          properties:
            authorization_token:
              type: string
              description: JWT encoded Authorization Token

    """

    data = request.json
    if not data:
        return {"message": "body should be json encoded object"}, 400
    if 'email' not in data:
        return {"message": "email field is required"}, 400

    if 'password' not in data:
        return {"message": "password field is required"}, 400

    try:
        token = auth_service.authenticate(data['email'], data['password'])
    except (AuthError, UserError) as e:
        print e
        return {"message": "invalid credentials"}, 401

    return {"authorization_token": token}, 201


@ctrlr.route("/auth/", methods=['GET'])
@jsonize
def auth_check_authenticated():
    """
    Checks authorization header.

    ---
    tags:
      - Auth
    security:
      - Bearer: []
    responses:
      200:
        description: Success
        schema:
          $ref: '#/definitions/User'
      400:
        description: Request is invalid.
      401:
        description: '`authorization_token` is invalid or expired.'
    definitions:
      - schema:
          id: User
          required:
            - email
            - token
            - created_on
            - updated_on
          properties:
            email:
              type: string
              description: User's email address
            token:
              type: string
              description: User's authorization token
            created_on:
              type: string
              description: Time when the user is created
            updated_on:
              type: string
              description: Time when the user is last updated

    """

    try:
        checked = auth_service.check_auth()
    except(UserError, AuthError):
        return {"message": "Not Authorized"}, 401
    return checked.to_dict(), 200
