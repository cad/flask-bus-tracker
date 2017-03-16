import json
import importlib
from sqlalchemy import create_engine
from api import app
from api.models import Model
from api.models.user import User
import config


def create_tables():
    engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
    Model.metadata.create_all(bind=engine)


def drop_tables():
    engine = create_engine(config.SQLALCHEMY_DATABASE_URI)
    Model.metadata.drop_all(bind=engine)


def create_superuser(email, password):
    dbs = app.DBSession
    user = User(
        email=email
    )
    user.set_password(password)
    dbs.add(user)
    dbs.commit()
    return user


def populate_fixture(path):
    dbs = app.DBSession
    total = 0
    with open(path) as f:
        json_data = json.loads(f.read())
        for item in json_data:
            fields = item['fields']
            classpath = item['class']
            modulepath = '.'.join(classpath.split('.')[:-1])
            classname = classpath.split('.')[-1]
            module = importlib.import_module(modulepath)
            cls = module.__getattribute__(classname)
            obj = cls(**fields)
            dbs.add(obj)
            try:
                dbs.commit()
                total += 1
            except Exception as e:
                dbs.rollback()
                print e
                print '-', fields

    print "  + {} items added!".format(total)
