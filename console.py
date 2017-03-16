#!/usr/bin/env python
from flask.ext.script import Manager, prompt_bool
from api import app, db, load_blueprints

manager = Manager(app)


@manager.command
def createdb():
    db.create_tables()
    print "Tables created!"


@manager.option('-f', '--file', help='Fixture file')
def populatedb(file):
    print "Populating..."
    db.populate_fixture(file)


#@manager.option('-p', '--password', help='User Password')
#@manager.option('-e', '--email', help='User Email')
@manager.command
def createsuperuser(email, password):
    user = db.create_superuser(email, password)
    print "Superuser created!"
    print user


@manager.command
def dropdb():
    if prompt_bool(
            "Are you sure you want to lose all your data"):
        db.drop_tables()
        print "Tables dropped!"


@manager.command
def runserver():
    load_blueprints(app)
    app.run(host='0.0.0.0')


if __name__ == "__main__":
    manager.run()
