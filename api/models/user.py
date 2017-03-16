import uuid
from passlib.hash import bcrypt
from sqlalchemy import Column, Integer, DateTime, String, func
from sqlalchemy.orm import validates
from api.models import Model


class User(Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String(128), unique=True)
    password = Column(String(40), unique=False)
    token = Column(String(256), nullable=True, default=None)

    created_on = Column(DateTime, default=func.now())
    updated_on = Column(DateTime, default=func.now(), onupdate=func.now())

    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)

    def __repr__(self):
        return "<User %r>" % (self.email)

    def set_password(self, password):
        """Salt and hash the provided password
        and put it into the model instance"""
        self.password = bcrypt.encrypt(password)

    def regenerate_token(self):
        self.token = uuid.uuid4().hex
        return self.token

    def check_password(self, password):
        return bcrypt.verify(password, self.password)

    def to_dict(self):
        d = {}
        for column in self.__table__.columns:  # pylint: disable=E1101
            if column.name == "password":
                continue
            if column.name == "id":
                continue
            d[column.name] = str(getattr(self, column.name))

        return d

    @validates('email')
    def validate_email(self, key, address):
        assert '@' in address, "There should be '@' in an email address!"
        return address
