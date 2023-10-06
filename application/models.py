from .database import db
from flask_login import login_manager   
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__="user"
    user_id=db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    user_name=db.Column(db.String,nullable=False,unique=True)
    password=db.Column(db.String,nullable=False)
    email=db.Column(db.String)
    follower_no=db.Column(db.Integer,default=0)
    post_no=db.Column(db.Integer,default=0)
    user_img=db.Column(db.LargeBinary)
    followers = db.relationship("Follower", backref="user", foreign_keys="Follower.user_id",lazy='dynamic',cascade='all, delete-orphan')
    
class Post(db.Model):
    __tablename__="posts"
    user_id = db.Column(db.Integer,   db.ForeignKey("user.user_id"), primary_key=True, nullable=False)
    post_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    image=db.Column(db.LargeBinary)
    content=db.Column(db.String,nullable=False)
    title=db.Column(db.String,nullable=False)

class Comment(db.Model):
    __tablename__="comments"
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey("posts.post_id"), nullable=False)
    comment_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    comment=db.Column(db.String,nullable=False)
    
class Like(db.Model):
    __tablename__="like"
    user_id = db.Column(db.Integer,   db.ForeignKey("user.user_id"), nullable=False)
    post_id = db.Column(db.Integer,   db.ForeignKey("posts.post_id"), nullable=False)
    like_id=db.Column(db.Integer, primary_key=True, autoincrement=True)

class Follower(db.Model):
    __tablename__="follower"
    id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer,   db.ForeignKey("user.user_id"), nullable=False)
    user_name=db.Column(db.String)
    follower_id= db.Column(db.Integer,   db.ForeignKey("user.user_id"), nullable=False)
    follower_name=db.Column(db.String)
    # user = db.relationship("User", foreign_keys=[user_id])
    # follow = db.relationship("User", foreign_keys=[follower_id])