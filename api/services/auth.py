from functools import wraps
from flask import request, redirect
from flask import current_app as app
from api.models.user import User
from api.exceptions.user import UserNotFound
from api.exceptions.auth import (
    AuthCredentialsInvalid, AuthHeaderMissing,
    AuthTokenMissing, AuthHeaderMalformed
)

dbs = app.DBSession


class AuthService():
    def authenticate(self, email, password):
        user = dbs.query(User).filter(User.email == email).first()
        if not user:
            raise UserNotFound

        if not user.check_password(password):
            raise AuthCredentialsInvalid

        token = user.regenerate_token()
        dbs.commit()
        return token

    def find_user_by_token(self, token):
        user = dbs.query(User).filter(User.token == token).first()
        return user

    def check_auth(self):
        header = request.headers.get('Authorization')
        if not header:
            raise AuthHeaderMissing
        token = self.__get_auth_token(header)
        if not token:
            raise AuthTokenMissing
        user = self.find_user_by_token(token)
        if not user:
            raise UserNotFound
        return user

    def check_token(self, token):
        user = self.find_user_by_token(token)
        if not user:
            return None
        return user

    def auth_required(self, func):
        @wraps(func)
        def decorated_function(*args, **kargs):
            checked = None
            try:
                checked = self.check_auth()
            except AuthHeaderMissing:
                print "AuthHeaderMissing"
            except AuthTokenMissing:
                print "AuthTokenMissing"
            except UserNotFound:
                print "UserNotFound"
            if not checked:
                return redirect('/auth/')

            return func(*args, **kargs)
        return decorated_function

    def __get_auth_token(self, header):
        auth = header
        if not auth:
            raise AuthHeaderMissing

        parts = auth.split()
        if parts[0].lower() != 'bearer':
            print(
                "Authorization header should be 'bearer'"
                "type but it is {} type."
                .format(parts[0].lower()))
            raise AuthHeaderMalformed
        elif len(parts) == 1:
            print(
                "Authorization header be consist of two parts"
                "seperated by a space.")
            raise AuthHeaderMalformed
        elif len(parts) > 2:
            print(
                "Authorization header be consist of two parts"
                "seperated by a space.")

            raise AuthHeaderMalformed

        token = parts[1]
        print token
        return token
