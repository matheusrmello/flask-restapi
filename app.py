from flask import Flask
from flask_restful import Api, Resource
from flask_mongoengine import MongoEngine 

app = Flask(__name__)
api = Api(app)
db = MongoEngine(app)


app.config["MONGODB_SETTINGS"] = [
    {
        "db": "users",
        "host": "mongodb",
        "port": 27017,
        "user": "root",
        "password": "123456admin"
    }
]

class User(db.Document):
    email = StringField(required=True)
    first_name = StringField(max_length=50)
    last_name = StringField(max_length=50)

class Users(Resource):
    def get(self):
        return {"message": "user 1"}, 200


class User(Resource):
    def get(self, cpf=None):
        if not cpf:
            return {"error": "CPF is required"}, 400
        return {"message": "CPF"}


api.add_resource(Users, '/users')
api.add_resource(User, '/user', '/user/<string:cpf>')

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
