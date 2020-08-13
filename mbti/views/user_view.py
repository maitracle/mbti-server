from flask import request, jsonify, Blueprint
from flask_jwt_extended import create_access_token

from mbti.models.users import User


user_view = Blueprint('user_view', __name__)


@user_view.route('/api/tokens', methods=['POST'])
def get_token():
    if not request.is_json:
        return jsonify({'message': 'Missing JSON in request'}), 400

    username = request.json.get('username', None)
    raw_password = request.json.get('password', None)

    token = User.get_token(username, raw_password)

    if token is '':
        return jsonify({'message': '아이디, 혹은 비밀번호가 정확하지 않습니다.'}), 401

    return jsonify(token=token), 200


@user_view.route('/api/users', methods=['POST'])
def sign_up():
    username = request.json.get('username')

    if User.is_exist_username(username):
        return jsonify({'message': '아이디가 중복되었습니다.'}), 400

    User.create_user(request.json)

    access_token = create_access_token(identity=username)

    return jsonify({'message': '유저 생성 성공', 'token': access_token}), 201
