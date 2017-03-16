#!/usr/bin/python
# coding: utf-8
import uuid
import datetime
from flask import (
    render_template,
    request, session,
    flash, url_for,
    redirect, make_response,
    after_this_request, g,
    abort, Response
)
from flask import current_app as app
from flask_swagger import swagger
from flask import jsonify # Swagger requirement
from api.helpers import jsonize

import config


@app.before_request
def before_request():
    pass


@app.after_request
def after_request(response):
    response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept, Authorization'
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, PATCH, DELETE, OPTIONS'
    return response


@app.teardown_request
def teardown_request(exception=None):
    dbs = app.DBSession
    dbs.remove()
    if exception and dbs.is_active:
        dbs.rollback()



@app.route("/", methods=['GET', 'POST'])
@jsonize
def api_root_view():
    links = []

    # poor man's api introspection
    for i in app.url_map.iter_rules():
        links.append((i.rule,  ",".join(list(i.methods))))

    return {
        'notice': "API Server",
        'version': config.API_VERSION,
        'endpoints': links}


@app.route("/spec")
def spec():
    swag = swagger(app)
    swag['info']['version'] = config.API_VERSION
    swag['info']['title'] = config.API_PROMPT
    swag['info']['description'] = config.API_DESCRIPTION
    swag['host'] = config.API_ROOT
    swag['basePath'] = '/'
    swag['produces'] = ("application/json",)
    swag['schemes'] = ("https", "http")
    swag['securityDefinitions'] = {"Bearer": {"type": "apiKey", "name": "Authorization", "in": "header"}}
    return jsonify(swag)


@app.route('/docs/')
def docs():
    return app.send_static_file('index.html')



# __all__ = ['Index', 'Product', 'Auth', 'ProductList', 'ProductAdmin']
