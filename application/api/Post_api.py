from flask_restful import Resource, Api,request
from flask import make_response,jsonify,Response,send_file,abort
from flask_restful import fields, marshal,request
from application.models import Post,User,Comment,Like
from application.database import db
from sqlalchemy import and_
import base64
import re
from flask_jwt_extended import jwt_required
class PostApi(Resource):
    # @jwt_required
    def get(self):
        posts = Post.query.all()
        image_responses = []
        for i in range(len(posts)):
            image =  base64.b64encode(posts[len(posts)-1-i].image)
            s1=str(image)
            output = re.findall(r"'(.*?)'", s1)[0]
            image_str="data:image;base64,"+output
            
            user_data=User.query.filter_by(user_id=posts[len(posts)-1-i].user_id).first()
            if(user_data.user_img):
                image =  base64.b64encode(user_data.user_img)
                s1=str(image)
                output = re.findall(r"'(.*?)'", s1)[0]
                user_image_str="data:image;base64,"+output
            else:
                user_image_str=""
            p_id=str(posts[len(posts)-1-i].post_id)
            like_data=Like.query.filter(and_(Like.post_id==p_id ,Like.user_id==7)).first()
            if(like_data ==None):
                like=False
            else:
                like=True
            image_responses.append({"username":user_data.user_name, 'user_img':user_image_str, 'image':image_str  , 'title': posts[len(posts)-1-i].title, 'content': posts[len(posts)-1-i].content ,'post_id': p_id ,'like':like})
        return image_responses
    def post(self):
        user_id = request.form['user_id']
        title = request.form['title']
        content = request.form['content']
        file = request.files['image']
        image = file.read()
        reg=Post(
        user_id=user_id,
        image=image,
        content=content,
        title=title
        )
        db.session.add(reg)
        db.session.commit()
        print("ok")
        return {'success': True}
class Get_post(Resource):
    def post(self):
        data=request.get_json()
        u_id=data["user_id"]
        posts = Post.query.all()
        image_responses = []
        for i in range(len(posts)):
            image =  base64.b64encode(posts[len(posts)-1-i].image)
            s1=str(image)
            output = re.findall(r"'(.*?)'", s1)[0]
            image_str="data:image;base64,"+output
            user_data=User.query.filter_by(user_id=posts[len(posts)-1-i].user_id).first()
            if(user_data.user_img):
                image =  base64.b64encode(user_data.user_img)
                s1=str(image)
                output = re.findall(r"'(.*?)'", s1)[0]
                user_image_str="data:image;base64,"+output
            else:
                user_image_str=""
            p_id=str(posts[len(posts)-1-i].post_id)
            like_data=Like.query.filter(and_(Like.post_id==p_id ,Like.user_id==u_id)).first()
            if(like_data !=None):
                like=True
            else:
                like=False
            image_responses.append({"user_id":user_data.user_id,"username":user_data.user_name, 'user_img':user_image_str, 'image':image_str  , 'title': posts[len(posts)-1-i].title, 'content': posts[len(posts)-1-i].content ,'post_id': p_id ,'like':like})
        return image_responses

class Comment_Api(Resource):
    def post(self):
        data=request.get_json()
        user_id=data["user_id"]
        post_id=data["post_id"]
        comment=data["comment"]
        add_comment=Comment(
        user_id=user_id,
        post_id=post_id,
        comment=comment
        )
        db.session.add(add_comment)
        db.session.commit()
        return {'success': True}

class Get_comment_Api(Resource):
    def post(self):
        data=request.get_json()
        post_id=data["post_id"]
        get_comment=Comment.query.filter_by(post_id=post_id).all()
        comment_responses = []
        for i in range(len(get_comment)):
            u_id=get_comment[len(get_comment)-1-i].user_id
            comt=get_comment[len(get_comment)-1-i].comment
            user_data = User.query.filter_by(user_id=u_id).first()
            if(user_data.user_img):
                image =  base64.b64encode(user_data.user_img)
                s1=str(image)
                output = re.findall(r"'(.*?)'", s1)[0]
                image_str="data:image;base64,"+output
            else:
                image_str=""
            comment_responses.append({"user_img":image_str,"u_name":user_data.user_name,"comment":comt})
        return comment_responses
    
class Like_Api(Resource):
    def post(self):
        data=request.get_json()
        user_id=data["user_id"]
        post_id=data["post_id"]
        add_like=Like(
        user_id=user_id,
        post_id=post_id,
        )
        db.session.add(add_like)
        db.session.commit()
        return {'success': True}
    
    def put(self):
        data=request.get_json()
        u_id=data["user_id"]
        p_id=data["post_id"]
        like_data=Like.query.filter(and_(Like.post_id==p_id ,Like.user_id==u_id)).delete()
        db.session.commit()
        return {'ok': 200}
    
class Get_like_Api(Resource):
    def post(self):
        data=request.get_json()
        user_id=data["user_id"]
        get_like=Like.query.filter_by(user_id=user_id).all()
        likes=[]
        for like in get_like:
            likes.append(like.post_id)
        return likes
    