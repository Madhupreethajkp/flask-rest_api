import sqlite3

import data as data
from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from models.user import UserModel

from datetime import date
from random import randint
from urllib.parse import quote
import webbrowser
today=date.today()


def get_id():
    income = (data['salary'] * 12)
    salary_per_year = int(income)
    if salary_per_year <= 500000:
        user_type_id = 'A'
    elif salary_per_year > 500000 & salary_per_year <= 1000000:
        user_type_id = 'B'
    elif salary_per_year > 1000000 & salary_per_year <= 1500000:
        user_type_id = 'C'
    elif salary_per_year > 1500000 & salary_per_year <= 3000000:
        user_type_id = 'D'
    elif salary_per_year > 3000000:
        user_type_id = 'E'
    i = 1
    while (i > 0):
        num = 1200 + i
    i = i + 1
    user_id = salary_per_year + '-' + num
    return user_id


def get_password():
    date = today.strftime("%d")
    month = today.sfrtime("%B")
    random_number = randint(100, 999)
    password = date + month + '-' + random_number
    return password


class UserRegister(Resource):
    TABLE_NAME = 'user_details'

    parser = reqparse.RequestParser()
    parser.add_argument('first_name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('last_name',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('date_of_birth',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('address',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('contact_no',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('email',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('qualification',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('gender',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('salary',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('pan_no',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('type_of_employer',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('name_of_employer',
                        type=str,
                        required=True,

                        )

    @jwt_required()
    def get(self, email):
        user = UserModel.find_by_email(email)
        if user:
            return user.json()
        return {'message': 'user not found'}, 404

    @property
    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_email(data['email']):
            return {"message": "User with that email id already exists."}, 400

        user_details = UserModel(data['first_name'], data['last_name'], data['date_of_birth'], data['address'], data[
            'contact_no'], data['email'], data['qualification'], data['gender'], data['salary'], data['pan_no'], data['type_of_employer']
                                 , data['name_of_employer'], get_id(), get_password())
        user_details.save_to_db()





        def mailto(recipients, subject, body):

            webbrowser.open("mailto:%s?subject=%s&body=%s" %
                            (recipients, quote(subject), quote(body)))

        body_template = """Dear User, 
                           Your User id is"+ user_id+ "and your password is "+password

           """

        def gen(email):
            mailto(email, "Hi!", body_template % locals())

        gen(data['email'])





        return {"message": "User created successfully."}, 201

    def delete(self, name):
        user = UserModel.find_by_email(email)
        if user:
            user.delete_from_db()
            return {'message': 'user deleted.'}
        return {'message': 'usernot found.'}, 404

class UserList(Resource):
    def get(self):
        return {'users': list(map(lambda x: x.json(), UserModel.query.all()))}


