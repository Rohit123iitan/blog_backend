from flask_restful import Resource, Api,request
from flask import json
from application.models import Follower,User
from application.database import db
class FollowerAPI(Resource):
    def post(self):
        data=request.get_json()
        user_id=data["user_id"]
        follower_id=data["follower_id"]
        user1=User.query.filter_by(user_id=user_id).first()
        follower1=User.query.filter_by(user_id=follower_id).first()
        if(user1==None or follower1==None):
            return []
        
        add_follow=Follower(
        user_id=user_id,
        user_name=user1.user_name,
        follower_id=follower_id,
        follower_name=follower1.user_name
        )
        print(add_follow)
        db.session.add(add_follow)
        db.session.commit()
        return {'success': True}

class Unfollow(Resource):
    def post(self):
        data=request.get_json()
        user_id=data["user_id"]
        follower_id=data["follower_id"]
        user=Follower.query.filter_by(user_id=user_id,follower_id=follower_id).delete()
        db.session.commit()
        return {'success': True}

class Get_follow(Resource):
    def post(self):
        data = request.get_json()
        user_id = data["user_id"]
        follows = Follower.query.filter_by(user_id=user_id).all()
        response = []
        for follow in follows:
            response.append({"name":follow.follower_name,"id":follow.follower_id})
        return response





        