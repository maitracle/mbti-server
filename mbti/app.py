from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from pymongo import MongoClient

from mbti.views.mbti_views import mbti_matcher_views
from mbti.views.user_views import user_views


app = Flask(__name__)

app.register_blueprint(user_views)
app.register_blueprint(mbti_matcher_views)

CORS(app)

production_db_info = 'mongodb://mbti-admin:TbP26SgDba7ZbEVpmrJMxJqTHfZsCcpj@13.124.34.75'
dev_db_info = 'localhost'

client = MongoClient(dev_db_info, 27017)
db = client.db_mbti

app.config['JWT_SECRET_KEY'] = 'XXXXX'  # Todo(maitracle): secret key를 환경변수에서 가져오게 수정한다.
jwt = JWTManager(app)

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)
