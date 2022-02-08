from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api =Api(app)

class SimpleCRUD(Resource):
    def get(self):
        return {'message': 'Simple get operation'}
    
    def post(self):
        return {'message': 'Simple post operation'}
    
    def put(self):
        return {'message': 'Simple put operation'}
    
    def delete(self):
        return {'message': 'Simple delete operation'}
    
api.add_resource(SimpleCRUD, '/')

if __name__ == '__main__':
    app.run(debug=True)
    