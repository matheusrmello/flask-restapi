from flask import jsonify
from flask_restful import Resource, reqparse
from mongoengine import NotUniqueError
from .model import UserModel
from loguru import logger
import re

logger.add("logs/app.log", retention="1 day", format="{time:DD-MM-YYYY at HH:mm:ss} | {level} | {message}")

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('first_name',
                          type=str,
                          required=True,
                          help='This field cannot be blank!'
                          )
_user_parser.add_argument('last_name',
                          type=str,
                          required=True,
                          help='This field cannot be blank!'
                          )
_user_parser.add_argument('cpf',
                          type=str,
                          required=True,
                          help='This field cannot be blank!'
                          )
_user_parser.add_argument('email',
                          type=str,
                          required=True,
                          help='This field cannot be blank!'
                          )
_user_parser.add_argument('birth_date',
                          type=str,
                          required=True,
                          help='This field cannot be blank!'
                          )


class Users(Resource):

    def get(self):
        logger.info("Getting all users")
        return jsonify(UserModel.objects())


class User(Resource):

    def validate_cpf(self, cpf):
        if not re.match(r'\d{3}\.\d{3}\.\d{3}-\d{2}', cpf):
            return False

        numbers = [int(digit) for digit in cpf if digit.isdigit()]

        if len(numbers) != 11 or len(set(numbers)) == 1:
            return False

        sum_of_products = sum(a * b for a, b in zip(numbers[0:9], range(10, 1, -1)))
        expected_digit = (sum_of_products * 10 % 11) % 10
        if numbers[9] != expected_digit:
            return False

        sum_of_products = sum(a * b for a, b in zip(numbers[0:10], range(11, 1, -1)))
        expected_digit = (sum_of_products * 10 % 11) % 10
        if numbers[10] != expected_digit:
            return False

        return True

    def post(self):
        data = _user_parser.parse_args()
        if not self.validate_cpf(data["cpf"]):
            result = {"message": "CPF is invalid!"}
            logger.warning("CPF validation failed: {data['cpf']}")
            return result, 400
        try:
            response = UserModel(**data).save()
            result = {"message": "User %s successfully created!" % response.id}
            logger.info("User %s successfully created!" % response.id)
            return result, 201
        except NotUniqueError:
            result = {"confict": "CPF already exist in database!"}
            logger.warning("CPF already exist in database")
            return result, 409

    def get(self, cpf):
        response = UserModel.objects(cpf=cpf)
        if response:
            return jsonify(response)
        result = {"message": "User does not exist in database!"}
        logger.error("message: User does not exist in database")
        return result, 404

    def delete(self, cpf):
        response = UserModel.objects(cpf=cpf)
        if response:
            response.delete()
            result = {"message": "User successfully deleted!"}
            logger.info("User successfully deleted")
            return result, 200
        else:
            result = {"message": "User already deleted in database!"}
            logger.warning("User not found in database")
            return result, 404

    def patch(self):
        data = _user_parser.parse_args()
        if not self.validate_cpf(data["cpf"]):
            result = {"message": "CPF is invalid!"}
            logger.warning("CPF validation failed: {data['cpf']}")
            return result, 400

        response = UserModel.objects(cpf=data["cpf"])
        if response:
            response.update(**data)
            result = {"message": "User successfully updated!"}
            logger.info("User successfully updated")
            return result, 200
        else:
            result = {"message": "User does not exist in database!"}
            logger.warning("User not found in database")
            return result, 404
