from flask_restful import Resource,request
from flask import make_response,jsonify
from application.validation import BusinessValidationError, NotFoundError
from application.models import User
from application.database import db
from werkzeug.security import generate_password_hash

class Res_Api(Resource):
    def post(self):
        data=request.get_json()
        username=data["username"]
        email=data["email"]
        new_password_=data["new_password"]
        password_=data["confirm_password"]
        password=generate_password_hash(password_)
        user=User.query.filter_by(user_name=username).first()
        if(len(password_)==0 or len(username)==0 or len(new_password_)==0):
            return {"result":'Something missing'}, 201
        if (new_password_!=password_):
            return {"result":'Check password'}, 203
        if not user :
            reg=User(
            user_name=username,
            password=password,
            email=email,
            follower_no=0,
            post_no=0,
            )
            db.session.add(reg)
            db.session.commit()
            return {"result":"Successfully Registered"},200
        else:
            if(user.password!=password_):
                print("124")
                return {'result' : 'Try with different username'}, 208
            return {"result":'You are already register.Please Log in'}, 202
            
        
    


    