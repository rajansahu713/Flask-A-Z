from flask import Flask
from flask_restful import Api
from info import info

app= Flask(__name__)

app.register_blueprint(info)

if __name__ =="__main__":
    app.run(debug=True)
