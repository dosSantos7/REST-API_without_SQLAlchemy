from flask import Flask
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from db import db


app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    # we don't want Flask's modification tracker
app.secret_key = "sudeep"  # needs to be complicated
api = Api(app)  # helps to make http operations easier

jwt = JWT(app, authenticate, identity)  # creates a new endpoint /auth which returns the JWT token

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
