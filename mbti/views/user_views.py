from flask import request, jsonify, Blueprint

from mbti.models.users import User


user_views = Blueprint('user_views', __name__)


@user_views.route('/api/tokens', methods=['POST'])
def get_token():
    if not request.is_json:
        return jsonify({'msg': 'Missing JSON in request'}), 400

    username = request.json.get('username', None)
    raw_password = request.json.get('password', None)

    token = User.get_token(username, raw_password)

    if token is '':
        return jsonify({'msg': '아이디, 혹은 비밀번호가 정확하지 않습니다.'}), 401

    return jsonify(token=token), 200


@user_views.route('/api/users', methods=['POST'])
def sign_up():
    username = request.json.get('username')
    password = request.json.get('password')

    if User.is_exist_username(username):
        return jsonify({'msg': '아이디가 중복되었습니다.'}), 400

    User.create_user(request.json)

    token = User.get_token(username, password)

    return jsonify({'msg': '유저 생성 성공', 'token': token}), 201
