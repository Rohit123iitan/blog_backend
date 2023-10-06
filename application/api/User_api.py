from flask_restful import Resource, Api,request
from flask import json
from application.models import User
from application.database import db
import base64
import re
from flask_jwt_extended import jwt_required
class UserApi(Resource):
    # @jwt_required
    def post(self):
        data=request.get_json()
        print(data)
        user_id=data["name"]
        user_data = User.query.filter_by(user_name=user_id).first()
        if(user_data.user_img):
            image =  base64.b64encode(user_data.user_img)
            s1=str(image)
            output = re.findall(r"'(.*?)'", s1)[0]
            image_str="data:image;base64,"+output
        else:
            image_str=""
        responses=[user_data.user_name,image_str,user_data.follower_no,user_data.post_no]
        return responses

class Search_user(Resource):
    def post(self):
        data=request.get_json()
        user_name=data["username"]
        users = User.query.filter(User.user_name.like(f'%{user_name}%')).all()
        response=[]
        for user in users:
            response.append({"username":user.user_name})
        return response
