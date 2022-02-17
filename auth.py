import re
from flask import Flask
from flask_restful import Resource, reqparse, fields, marshal_with,Api
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


app=Flask(__name__)
api = Api(app)

app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///auth.db'

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(50))

user_post_parser = reqparse.RequestParser()
user_post_parser.add_argument('username', type=str, required=True, help='Name cannot be blank!')
user_post_parser.add_argument('password', type=str, required=True, help='Password cannot be blank!')

user_fields = {
    'username': fields.String,
    'password': fields.String
}    

db.create_all()

class Users(Resource):
    @marshal_with(user_fields)
    def get(self):
        user =User.query.all()
        return user, 200

    @marshal_with(user_fields)
    def post(self):
        data = user_post_parser.parse_args()
        hash_password = generate_password_hash(data['password'], method='sha256')
        new_user = User(username=data['username'], password=hash_password)
        db.session.add(new_user)
        db.session.commit()
        return new_user, 201

class Login(Resource):
    def post(self):
        data = user_post_parser.parse_args()
        user = User.query.filter_by(username=data['username'], password= data["password"]).first()
        print(user)
        if user:   
            return {'message': 'Login successful'}, 200
        return {'message': 'Invalid username or password'}, 401
    

api.add_resource(Users, '/users')
api.add_resource(Login, '/login')

if __name__ == '__main__':
    app.run(debug=True)



