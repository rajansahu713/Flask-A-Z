from tkinter.messagebox import NO
from flask import Flask
from flask_restful import Resource, Api, reqparse, marshal_with, fields
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///banking.db"


db = SQLAlchemy(app)


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(80), nullable=False)
    user_email = db.Column(db.String(120), unique=True, nullable=False)
    user_phone = db.Column(db.String(120), unique=True, nullable=False)
    


class Account(db.Model):
    account_number = db.Column(db.Integer, primary_key=True)
    account_name = db.Column(db.String(80), nullable=False)
    account_balance = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    user = db.relationship('User', backref=db.backref('accounts', lazy=True))

#db.create_all()

user_post_parser = reqparse.RequestParser()
user_post_parser.add_argument('user_name', type=str, required=True, help='Name is required')
user_post_parser.add_argument('user_email', type=str, required=True, help='Email is required')
user_post_parser.add_argument('user_phone', type=str, required=True, help='Phone is required')

user_patch_parser = reqparse.RequestParser()
user_patch_parser.add_argument('user_name', type=str, required=False, help='Name is required')
user_patch_parser.add_argument('user_email', type=str, required=False, help='Email is required')
user_patch_parser.add_argument('user_phone', type=str, required=False, help='Phone is required')


account_post_parser = reqparse.RequestParser()
account_post_parser.add_argument('account_name', type=str, required=True, help='Name is required')
account_post_parser.add_argument('account_balance', type=int, required=True, help='Balance is required')
account_post_parser.add_argument('user_id', type=int, required=True, help='User id is required')

account_patch_parser = reqparse.RequestParser()
account_patch_parser.add_argument('account_name', type=str, required=False, help='Name is required')
account_patch_parser.add_argument('account_balance', type=int, required=False, help='Balance is required')
account_patch_parser.add_argument('user_id', type=int, required=True, help='User id is required')


account_fields = {
    'account_number': fields.Integer,
    'account_name': fields.String,
    'account_balance': fields.Integer,
    'user_id': fields.Integer,
}

account_fields_without_user_id = {
    'account_number': fields.Integer,
    'account_name': fields.String,
    'account_balance': fields.Integer,
}

user_fields = {
    'user_id': fields.Integer,
    'user_name': fields.String,
    'user_email': fields.String,
    'user_phone': fields.String,
    "accounts": fields.Nested(account_fields_without_user_id)
}




class UserList(Resource):
    """
    API End point to get all users and particular user
    for particular user you need to provide user id in urls
    """
    @marshal_with(user_fields)
    def get(self, id =None):
        if id is not None: 
            user = User.query.filter_by(user_id=id).first()
            return user
            
        users = User.query.all()
        return users

    def post(self):
        """
        API End point to create new user
        """
        args = user_post_parser.parse_args()
        print(args['user_name'])
        user = User(user_name=args['user_name'], user_email=args['user_email'], user_phone=args['user_phone'])
        db.session.add(user)
        db.session.commit()
        return {"message":"New record created"}, 201

    
    def delete(self, id=None):
        """
        API End point to delete user
        """
        if id is not None:
            try:
                user = User.query.filter_by(user_id=id).first()
                db.session.delete(user)
                db.session.commit()
                return {"message":"Record successfully Delete"}, 201
            except:
                return {"message":"Record not found"}, 404
        else:
            return {"message":"Id is required"}, 400

    def put(self, id=None):
        """
        API End point to update user
        """
        if id is not None:
            user = User.query.filter_by(user_id=id).first()
            if user is not None:
                args = user_post_parser.parse_args()
                print(args)
                user.user_name = args['user_name']
                user.user_email = args['user_email']
                user.user_phone = args['user_phone']
                db.session.commit()
                return {"message":"Record successfully updated"}, 201
            return {"message":"Record not found"}, 404
        else:
            return {"message":"Id is required"}, 400

    def patch(self, id=None):
        """
        API End point to update user partially
        """
        if id is not None:
            try:
                user = User.query.filter_by(user_id=id).first()
                args = user_patch_parser.parse_args()
                if args['user_name'] is not None:
                    user.user_name = args['user_name']
                if args['user_email'] is not None:
                    user.user_email = args['user_email']
                if args['user_phone'] is not None:
                    user.user_phone = args['user_phone']
                db.session.commit()
                return {"message":"Record successfully updated"}, 201
            except:
                return {"message":"Record not found"}, 404

class AccountList(Resource):
    @marshal_with(account_fields)
    def get(self, id=None):
        """
        API End point to get all accounts and particular account
        """
        if id is not None:
            try:
                account = Account.query.filter_by(account_number=id).first()
                return account, 200
            except:
                return {"message":"Particular account id is not found"}, 404
            
        else:
            accounts = Account.query.all()
            return accounts, 200

    def post(self):
        """
        API End point to create new account
        """
        args = account_post_parser.parse_args()
        account = Account(account_name=args['account_name'], account_balance=args['account_balance'], user_id=args['user_id'])
        db.session.add(account)
        db.session.commit()
        return {"message":"New record created"}, 201

    def delete(self, id=None):
        """
        API End point to delete account
        """
        if id is not None:
            try:
                account = Account.query.filter_by(account_number=id).first()
                db.session.delete(account)
                db.session.commit()
                return {"message":"Record successfully Delete"}, 201
            except:
                return {"message":"Record not found"}, 404
        else:
            return {"message":"Id is required"}, 400

    def patch(self, id=None):
        """
        API End point to update account
        """
        if id is not None:
            account = Account.query.filter_by(account_number=id).first()
            if account is not None:
                args = account_patch_parser.parse_args()
                if args['account_name'] is not None:
                    account.account_name = args['account_name']
                if args['account_balance'] is not None:
                    account.account_balance = args['account_balance']
                if args['user_id'] is not None:
                    account.user_id = args['user_id']
                db.session.commit()
                return {"message":"Record successfully updated"}, 201
            return {"message":"Record not found"}, 404
        else:
            return {"message":"Id is required"}, 400

api.add_resource(UserList, '/users', '/users/<int:id>')
api.add_resource(AccountList, '/accounts', '/accounts/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)


        
        



    


