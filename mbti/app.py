from flask import Flask
from flask_jwt_extended import JWTManager
from pymongo import MongoClient

from mbti.views.user_view import user_view


app = Flask(__name__)
app.register_blueprint(user_view)

client = MongoClient('localhost', 27017)
db = client.db_mbti

app.config['JWT_SECRET_KEY'] = 'secret-key-need'  # Change this!
jwt = JWTManager(app)


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)

# asdf
