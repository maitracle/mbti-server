from flask import Flask
from flask_jwt_extended import JWTManager
from pymongo import MongoClient

from mbti.views.mbti_views import mbti_matcher_views
from mbti.views.user_views import user_views


app = Flask(__name__)
app.register_blueprint(user_views)
app.register_blueprint(mbti_matcher_views)

production_db_info = 'mongodb://mbti-admin:TbP26SgDba7ZbEVpmrJMxJqTHfZsCcpj@13.124.34.75'
dev_db_info = 'localhost'

client = MongoClient(dev_db_info, 27017)
db = client.db_mbti

app.config['JWT_SECRET_KEY'] = 'g#*5q+!l0tglppmfq9gq-h7w3o(7te**j8jjq8rsqad^&nbjcd'  # Change this!
jwt = JWTManager(app)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
