from flask import Flask
from flask_restful import Resource, Api, reqparse, marshal_with, fields
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False,)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(120), unique=True, nullable=False)

db.create_all()

student_fields = {
    'id': fields.Integer,
    'name': fields.String,
    'email': fields.String,
    'phone': fields.String,
}

student_registration_parser = reqparse.RequestParser()
student_registration_parser.add_argument('name', type=str, required=True, help='Name is required')
student_registration_parser.add_argument('email', type=str, required=True, help='Email is required')
student_registration_parser.add_argument('phone', type=str, required=True, help='Phone is required')


class StudentList(Resource):
    @marshal_with(student_fields)
    def get(self, id=None):
        if id is not None:
            student = Student.query.filter_by(id=id).first()
            if student:
                return student, 200
            else:
                return Student.query.all(), 404

        return Student.query.all()

    def post(self):
        args = student_registration_parser.parse_args()
        student = Student(name=args['name'], email=args['email'], phone=args['phone'])
        db.session.add(student)
        db.session.commit()
        return {'message': 'Student created successfully'}, 201

    def put(self, id=None):
        if id is None:
            return {'message': 'Student id is required'}, 400
        args = student_registration_parser.parse_args()
        student = Student.query.filter_by(id=id).first()
        if student:
            student.name = args['name']
            student.email = args['email']
            student.phone = args['phone']
            db.session.commit()
            return {'message': 'Student updated successfully'}, 200
        else:
            return {'message': 'Student not found'}, 404


    def patch(self, id=None):
        if id is None:
            return {'message': 'Student id is required'}, 400
        args = student_registration_parser.parse_args()
        student = Student.query.filter_by(id=id).first()
        if student:
            student.name = args['name'] if args['name'] else student.name
            student.email = args['email'] if args['email'] else student.email
            student.phone = args['phone'] if args['phone'] else student.phone
            db.session.commit()
            return {'message': 'Student updated successfully'}, 200
        else:
            return {'message': 'Student not found'}, 404

    def delete(self, id=None):
        if id is None:
            return {'message': 'Student id is required'}, 400
        student = Student.query.filter_by(id=id).first()
        if student:
            db.session.delete(student)
            db.session.commit()
            return {'message': 'Student deleted successfully'}, 204
        else:
            return {'message': 'Student not found'}, 404


api.add_resource(StudentList, '/students', '/students/<int:id>')


if __name__ == "__main__":
    app.run(debug=True)

