#!/usr/bin/python
from os import getenv as _getenv

DEBUG = True
SESSION_BACKEND = 'inmem'  # in memory kv store
API_VERSION = 'devel'
API_PROMPT = "Bus Tracker API Server"
API_DESCRIPTION = "Tracking the buses for you since 2017."
API_ROOT = '127.0.0.1:5000'
SQLALCHEMY_DATABASE_URI = 'sqlite:///data/bus-tracker.db'

# if there is environment variable prefixed with _prefix, override above
# variables only upper-case variables without underscore prefix will be
# overriden it might be useful to export environment variables
# in a -gitignored- *.conf file then source it
_prefix = "BUSTRACKER_"
_locals = locals()
_config_variables = filter(
    lambda x: not x.startswith('_') and x.isupper(), _locals.keys())

for _variable in _config_variables:
    _locals[_variable] = _getenv(_prefix + _variable, _locals[_variable])
