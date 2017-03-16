from api import app, load_blueprints
app = app
with app.app_context():
    load_blueprints(app)
