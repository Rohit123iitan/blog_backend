import os
from flask import Flask,jsonify
from flask_restful import Resource, Api
from application import config
from application.config import LocalDevelopmentConfig
from application.database import db
from flask_cors import CORS
# from application.models import User
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
app = None
api = None

def create_app():
    app = Flask(__name__)
    if os.getenv('ENV', "development") == "production":
      raise Exception("Currently no production config is setup.")
    else:
      print("Staring Local Development")
      app.config.from_object(LocalDevelopmentConfig)
    db.init_app(app)
    app.app_context().push()
    api = Api(app)
    jwt = JWTManager(app)
    app.app_context().push()
    CORS(app)
    return app, api

app,api = create_app()
from application.api.Registration_api import Res_Api
api.add_resource(Res_Api, "/api/registration")
from application.api.Post_api import PostApi
api.add_resource(PostApi,"/api/blog_post","/api/get_all_blog")
from application.api.Post_api import Get_post
api.add_resource(Get_post,"/api/get_blog")
from application.api.login_api import LoginApi
api.add_resource(LoginApi,"/api/login")
from application.api.User_api import UserApi
api.add_resource(UserApi,"/api/get_user_data")
from application.api.Post_api import Comment_Api
api.add_resource(Comment_Api,"/api/add_comment")
from application.api.Post_api import Get_comment_Api
api.add_resource(Get_comment_Api,"/api/get_comment")
from application.api.Post_api import Like_Api
api.add_resource(Like_Api,"/api/like_post","/api/dislike_post")
from application.api.Post_api import Get_like_Api
api.add_resource(Get_like_Api,"/api/get_user_like")
from application.api.User_api import Search_user
api.add_resource(Search_user,"/api/search")
from application.api.Follower_api import FollowerAPI
api.add_resource(FollowerAPI,"/api/follow")
from application.api.Follower_api import Get_follow
api.add_resource(Get_follow,"/api/get_follower")

if __name__ == '__main__':
  app.run(host='0.0.0.0',port=8080)
