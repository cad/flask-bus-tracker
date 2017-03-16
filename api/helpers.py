try:
    from json import dumps, dump
except ImportError:
    from simplejson import dumps, dump
import json
from flask import Response
from flask import Flask, jsonify
from functools import wraps
#from datetime import datetime


def make_json_app(import_name, **kwargs):
    """
    handle exceptions as json outputs
    """
    from werkzeug.exceptions import default_exceptions
    from werkzeug.exceptions import HTTPException

    def make_json_error(ex):
        response = jsonify(message=str(ex))
        response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept, Authorization'
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.status_code = (ex.code
                                if isinstance(ex, HTTPException)
                                else 500)
        return response

    app = Flask(import_name, **kwargs)

    for code in default_exceptions.iterkeys():
        app.error_handler_spec[None][code] = make_json_error

    return app


class _DateEncoder(json.JSONEncoder):
    def default(self, obj):
        # if hasattr(obj, 'isoformat'):
        #     epoch = (obj.replace(tzinfo=None) - datetime(1970,1,1)).total_seconds()

        #     return epoch
        # else:
        return str(obj)
        #return json.JSONEncoder.default(self, obj)

def jsonize(func):
    """
    flask view decorator that takes care of tuple responses
    adds extra layers and makes them json.
    With that ou can do things like:

    return {'something': 'some other thing}, 200
    """
    @wraps(func)
    def decorated_view(*args, **kwargs):

        result, code = {}, 200

        r  = func(*args, **kwargs)
        if isinstance(r, tuple) and len(r) > 1:
            result, code = r
        elif isinstance(r, dict):
            result = r
        # appendix = {'':''}
        # result.update(appendix)

        return Response(dumps(result,indent=4, cls=_DateEncoder), mimetype='application/json', status=code)
    return decorated_view
