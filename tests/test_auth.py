# coding: utf-8
""" Auth endpoints unit tests"""

import pytest
import json as _json


def unjson(s):
    return _json.loads(s)


def json(d):
    return _json.dumps(d)


def test_get_authorization_token(client, user_service, auth_service):
    user = dict(email="test@test.test", password="1234")
    user_service.create(user['email'], user['password'])
    rv = client.post('/auth/',
                     data=json(user),
                     content_type='application/json',
                     follow_redirects=True)

    assert rv.status_code == 201
    data = unjson(rv.data)
    assert 'authorization_token' in data
    assert auth_service.check_token(data['authorization_token'])


def test_access_protected_resource(client, user_service, auth_service):
    user = dict(email="test@test.test", password="1234")
    user_service.create(user['email'], user['password'])
    token = auth_service.authenticate(user['email'], user['password'])
    assert token

    rv = client.get('/auth/',
                    headers={'Authorization': 'Bearer {token}'.format(token=token)},
                    content_type='application/json',
                    follow_redirects=True)

    assert rv.status_code == 200


def test_access_protected_resource_failure(client, user_service, auth_service):
    token = "asd"
    rv = client.get('/auth/',
                    headers={'Authorization': 'Bearer {token}'.format(token=token)},
                    content_type='application/json',
                    follow_redirects=True)

    assert rv.status_code == 401
