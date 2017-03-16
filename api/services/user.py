from flask import current_app as app
from api.models.user import User
from api.exceptions.user import (
    UserNotFound, UserAlreadyExists, UserUnknownError
)

dbs = app.DBSession


class UserService():
    def get(self, email, silent=False):
        user = dbs.query(User).filter(
            User.email == email).first()
        if not user:
            if silent:
                return None
            raise UserNotFound
        user_dict, errors = user.dump()
        if errors:
            raise UserUnknownError(errors)
        return user_dict

    def create(self, email, password):
        user = User()
        user.email = email
        user.is_approved = False
        user.set_password(password)
        existing_user = self.get(user.email, silent=True)
        if existing_user:
            raise UserAlreadyExists
        dbs.add(user)
        dbs.commit()
        return user.to_dict()

    def set_password(self, email, password):
        user = self.get(email)
        user.set_password(password)
        dbs.commit()
