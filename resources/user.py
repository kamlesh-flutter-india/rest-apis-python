from datetime import timedelta
from flask import app, jsonify, request
from flask.views import MethodView
from flask_smorest import Blueprint,abort
from passlib.hash import pbkdf2_sha256
from flask_jwt_extended import create_access_token, get_jwt, jwt_required, create_refresh_token, get_jwt_identity

from blocklist import BLOCKLIST
from db import db
from sqlalchemy.exc import SQLAlchemyError
from models.user import UserModel
from schemas import UserScehema

blp = Blueprint("Users", 'users',description='Operations on users')

@blp.route("/register")
class UserRegister(MethodView):
    @blp.arguments(UserScehema)
    def post(self,user_data):
        if UserModel.query.filter(UserModel.username == user_data['username']).first():
            abort(409,message='A user with username already exists.')
        user = UserModel(
           username = user_data['username'],
           password = pbkdf2_sha256.hash(user_data['password'])
           )
        db.session.add(user)
        db.session.commit()
        return {'message': 'User Created Successfully!'},201
    
@blp.route('/login')
class UserLogin(MethodView):
    @blp.arguments(UserScehema)
    def post(self,user_data):
        user = UserModel.query.filter(
            UserModel.username == user_data['username']
        ).first()
        if user and pbkdf2_sha256.verify(user_data['password'], user.password):
            access_token = create_access_token(identity=str(user.id),expires_delta=timedelta(hours=1),fresh=True)
            refresh_token = create_refresh_token(identity=str(user.id))
            return jsonify({"access_token": access_token,"refresh_token": refresh_token})

        abort(401,message='inavalid username or password')

@blp.route('/logout')
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']
        BLOCKLIST.add(jti)
        return {"message": "Success"}
    
@blp.route('/user/<int:user_id>')
class User(MethodView):
    @blp.response(200,UserScehema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user
    
    def delete(self,user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": 'User deleted successfully'},200
    
@blp.route('/refresh')
class TokenRefresh(MethodView):
    @jwt_required(refresh=True)
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=str(current_user),expires_delta=timedelta(hours=1),fresh=False)
        return jsonify({"access_token": new_token})