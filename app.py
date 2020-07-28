from flask import Flask
from flask_restful import Api

from resources.user import UserRegister
from resources.user import UserList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'madhu'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


api = Api(app)

api.add_resource(UserRegister, '/register')
#api.add_resource(UserList, '/user/<string:email>')

api.add_resource(UserList, '/users')
# api.add_resource(PolicyRegister, '/policyregister')


if __name__ == '__main__':
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)