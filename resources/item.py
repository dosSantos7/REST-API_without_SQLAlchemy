import sqlite3

from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.item import ItemModel


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="This field is mandatory."
                        )

    @jwt_required()
    def get(self, name):
        item = ItemModel.get_by_name(name)
        if item:
            return item.json()
        return {'message': "couldn't find item."}

    def post(self, name):
        if ItemModel.get_by_name(name):
            return {'message': 'Item with name {} already exists.'.format(name)}, 400  # bad request

        data = Item.parser.parse_args()
        item = ItemModel(name, data['price'])
        try:
            item.insert()
        except:
            return {'message': 'An error occurred while inserting the item.'}, 500  # internal server error

        return item.json(), 201  # item in JSON format is returned

    # place all items which don't match name & replace original items
    def delete(self, name):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "DELETE FROM items WHERE name=?"
        cursor.execute(query, (name,))

        connection.commit()
        connection.close()
        return {'message': f"{name} deleted successfully."}

    # create or update existing with PUT
    def put(self, name):

        data = Item.parser.parse_args()
        item = ItemModel.get_by_name(name)
        updated_item = ItemModel(name, data['price'])
        if item:
            try:
                updated_item.update()
            except:
                return {'message': 'An error occurred while updating item.'}, 500  # internal server error
        else:
            try:
                updated_item.insert()
            except:
                return {'message': 'An error occurred while inserting item.'}, 500  # internal server error

        return updated_item.json()


class ItemList(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cursor = connection.cursor()

        query = "SELECT * FROM items"
        result = cursor.execute(query)

        items = []
        for row in result.fetchall():
            items.append({'name': row[0], 'price': row[1]})

        connection.close()

        return {'all_items': items}
