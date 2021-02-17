import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username', type=str, required=True, help="Username can't be blank!!")
    parser.add_argument('password', type=str, required=True, help="Password can't be blank!!")

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {'message': 'A user with same username already exists.'}, 400

        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        # for auto-incrementing values we dont need to pass anything, so NULL
        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(query, (data['username'], data['password']))

        connection.commit()
        connection.close()

        return {'message': 'User registered successfully!!'}, 201
