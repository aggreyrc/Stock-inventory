#!/usr/bin/env python3

# Standard library imports

# Remote library imports
from flask import request, Flask,jsonify,make_response
from flask_restful import Resource, Api, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS


# Local imports
# from config import app, db, api
# Add your model imports
from models import db

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

api = Api(app)

CORS(app)

# Views go here!

class Home(Resource):
    def get(self):
        return '<h1>Project Server</h1>'
    
api.add_resource(Home, '/')


if __name__ == '__main__':
    app.run(port=5555, debug=True)

