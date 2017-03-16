import logging
import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask import _app_ctx_stack

logging.basicConfig(level=logging.DEBUG)

try:
    from json import dumps, dump
except ImportError:
    from simplejson import dumps, dump
import json
from flask import Response
from flask import Flask, jsonify
from functools import wraps
#from datetime import datetime
from api import load_blueprints
from api.models import Model
from api.models.user import User

def make_json_app(import_name, **kwargs):
    """
    handle exceptions as json outputs
    """
    from werkzeug.exceptions import default_exceptions
    from werkzeug.exceptions import HTTPException

    def make_json_error(ex):
        response = jsonify(message=str(ex))
        response.status_code = (ex.code
                                if isinstance(ex, HTTPException)
                                else 500)
        return response

    app = Flask(import_name, **kwargs)

    for code in default_exceptions.iterkeys():
        app.error_handler_spec[None][code] = make_json_error

    return app


@pytest.yield_fixture(scope="session")
def app():
    _app = make_json_app("test")
    _app.config.from_object('config')
    ctx = _app.app_context()
    ctx.push()

    _app.engine = create_engine("sqlite://",
                                encoding='utf8', convert_unicode=True)
    _app.DBSession = scoped_session(
        sessionmaker(),
        scopefunc=_app_ctx_stack.__ident_func__
    )

    _app.DBSession.configure(bind=_app.engine)

    _app.connection = _app.engine.connect()

    load_blueprints(_app)
    yield _app

    # teardown
    _app.connection.close()
    ctx.pop()


@pytest.yield_fixture(scope="function")
def client(app):
    Model.metadata.create_all(bind=app.engine)
    client = app.test_client()
    yield client
    Model.metadata.drop_all(bind=app.engine)


@pytest.fixture
def user_service(app):
    from api.services.user import UserService
    return UserService()


@pytest.fixture
def auth_service(app):
    from api.services.auth import AuthService
    return AuthService()
