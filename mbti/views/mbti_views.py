from flask import jsonify, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity

from mbti.mbti_matcher import MbtiMatcher
from mbti.models.users import User


mbti_matcher_views = Blueprint('mbti_matcher_views', __name__)


@mbti_matcher_views.route('/api/mbti/match-user', methods=['GET'])
@jwt_required
def get_matched_user():
    request_username = get_jwt_identity()
    user = User.get_user_by_username(request_username)

    if not MbtiMatcher.is_available_match(user):
        return jsonify({'msg': '매칭은 하루에 한번 가능합니다. 내일 다시 시도해주세요.'}), 400

    matched_user = MbtiMatcher.match(user)

    if not matched_user:
        return jsonify({'msg': '조건에 맞는 상대방이 존재하지 않습니다.'}), 400

    return jsonify({'msg': '', 'matched_user': matched_user}), 200
