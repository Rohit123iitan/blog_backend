from flask_restful import Resource, Api,request
from flask import jsonify
from flask_restful import reqparse
from application.validation import BusinessValidationError, NotFoundError
from application.models import User
from application.database import db
from flask_jwt_extended import create_access_token
from werkzeug.security import check_password_hash
class LoginApi(Resource):
    def post(self):
        data=request.get_json()
        username=data["username"]
        password_=data["password"]
        user_=User.query.filter_by(user_name=username).first()
        if not user_:
            return {"msg": "Invalid user."}, 401
        if not check_password_hash(user_.password, password_):
            return {"msg": "Invalid password."}, 402
        else:
            access_token = create_access_token(identity=username)
            user_data=[access_token,user_.user_id]
            return user_data
        