# coding: utf-8
import os
import sys
sys.path.append(os.path.join(os.path.dirname(
    os.path.abspath(__file__)
), '../'))

from flask import Flask, jsonify
from flask import _app_ctx_stack
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine
from helpers import make_json_app
import config

app = make_json_app(__name__)
app.config.from_object('config')
app.engine = create_engine(app.config["SQLALCHEMY_DATABASE_URI"],
                           encoding='utf8', convert_unicode=True)
app.DBSession = DBSession = scoped_session(
    sessionmaker(),
    scopefunc=_app_ctx_stack.__ident_func__
)

app.DBSession.configure(bind=app.engine)
#if app.config['DEBUG']:
    #from werkzeug.contrib.profiler import ProfilerMiddleware
    #app.config['PROFILE'] = True
    #app.wsgi_app = ProfilerMiddleware(app.wsgi_app, restrictions=[30])

def load_blueprints(app):
    # Session settings
    if config.SESSION_BACKEND == 'inmem':
        from _session_backends import inmem_backend
        store = inmem_backend.DictStore()
        # Replacing flask's stock session back-end
        inmem_backend.KVSessionExtension(store, app)

    app.secret_key = os.urandom(24)  # put this in config
    app.debug = True

    from api.controllers import auth
    app.register_blueprint(auth.controller)
