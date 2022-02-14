from enum import unique
from flask import Flask
from flask_restful import Resource, Api, reqparse, marshal_with, fields
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///student.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db =SQLAlchemy(app)

class Student(db.Model):
    roll_no = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(120), unique=True, nullable=False)
    house = db.relationship('House',uselist=False, backref='student')

class House(db.Model):
    House_id = db.Column(db.Integer, primary_key=True)
    floor = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(80), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('student.roll_no'), nullable=False)
    

db.create_all()
student_post_parser = reqparse.RequestParser()
#student_post_parser.add_argument('roll_no', type=int, required=True, help='Name is required')
student_post_parser.add_argument('name', type=str, required=True, help='Address is required')
student_post_parser.add_argument('address', type=str, required=True, help='Phone is required')

student_patch_parser = reqparse.RequestParser()
student_patch_parser.add_argument('name', type=str, required=False, help='Name is required')
student_patch_parser.add_argument('address', type=str, required=False, help='Address is required')

house_post_parser = reqparse.RequestParser()
house_post_parser.add_argument('floor', type=int, required=True, help='Name is required')
house_post_parser.add_argument('name', type=str, required=True, help='Address is required')
house_post_parser.add_argument('student_id', type=int, required=True, help='Phone is required')


house_patch_parser = reqparse.RequestParser()
house_patch_parser.add_argument('floor', type=int, required=False, help='Name is required')
house_patch_parser.add_argument('name', type=str, required=False, help='Address is required')
house_patch_parser.add_argument('student_id', type=int, required=False, help='Phone is required')


house_fields = {
    'House_id': fields.Integer,
    'floor': fields.Integer,
    'name': fields.String,
    'student_id': fields.Integer,
}

students_fields = {
    'roll_no': fields.Integer,
    'name': fields.String,
    'address': fields.String,
    'house': fields.Nested(house_fields)
}


class Student_CRUD(Resource):
    @marshal_with(students_fields)
    def get(self, id=None):
        if id is not None:
            student = Student.query.filter_by(id=id).first()
            if student:
                return student, 200
            else:
                return Student.query.all(), 404

        return Student.query.all()

    def post(self):
        try:
            args = student_post_parser.parse_args()
            print(args)
            student = Student(name=args['name'], address=args['address'])
            print(student)
            db.session.add(student)
            db.session.commit()
            return {'message': 'Student created successfully'}, 201
        except:
            return {'message': 'Something went wrong'}, 500

    def delete(self, id=None):
        try:
            student = Student.query.filter_by(id=id).first()
            if student:
                db.session.delete(student)
                db.session.commit()
                return {'message': 'Student deleted successfully'}, 200
            else:
                return {'message': 'Student not found'}, 404
        except:
            return {'message': 'Something went wrong'}, 500

    def patch(self, id=None):
        try:
            args = student_patch_parser.parse_args()
            student = Student.query.filter_by(id=id).first()
            if student:
                if args['name']:
                    student.name = args['name']
                if args['address']:
                    student.address = args['address']
                db.session.commit()
                return {'message': 'Student updated successfully'}, 200
            else:
                return {'message': 'Student not found'}, 404
        except:
            return {'message': 'Something went wrong'}, 500

class House_CRUD(Resource):
    @marshal_with(house_fields)
    def get(self, id=None):
        if id is not None:
            house = House.query.filter_by(id=id).first()
            if house:
                return house, 200
            else:
                return House.query.all(), 404

        return House.query.all()
    
    def post(self):
        try:
            args = house_post_parser.parse_args()
            print(args)
            house = House(floor=args['floor'], name=args['name'], student_id=args['student_id'])
            print(house)
            db.session.add(house)
            db.session.commit()
            return {'message': 'House created successfully'}, 201
        except:
            return {'message': 'Something went wrong'}, 500

    def delete(self, id=None):
        try:
            house = House.query.filter_by(id=id).first()
            if house:
                db.session.delete(house)
                db.session.commit()
                return {'message': 'House deleted successfully'}, 200
            else:
                return {'message': 'House not found'}, 404
        except:
            return {'message': 'Something went wrong'}, 500

    
    def patch(self, id=None):
        try:
            args = house_patch_parser.parse_args()
            house = House.query.filter_by(id=id).first()
            if house:
                if args['floor']:
                    house.floor = args['floor']
                if args['name']:
                    house.name = args['name']
                if args['student_id']:
                    house.student_id = args['student_id']
                db.session.commit()
                return {'message': 'House updated successfully'}, 200
            else:
                return {'message': 'House not found'}, 404
        except:
            return {'message': 'Something went wrong'}, 500



api.add_resource(Student_CRUD, '/student', '/student/<int:id>')
api.add_resource(House_CRUD, '/house', '/house/<int:id>')


if __name__=='__main__':
    app.run(debug=True)

