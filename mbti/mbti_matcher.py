from datetime import datetime


mbti_map = {
    'INFP': ['ENFJ', 'ENTJ'],
    'ENFP': ['INFJ', 'INTJ'],
    'INFJ': ['ENFP', 'ENTP'],
    'ENFJ': ['INFP', 'ISFP'],
    'INTJ': ['ENFP', 'ENTP'],
    'ENTJ': ['INFP', 'INTP'],
    'INTP': ['ENTJ', 'ESTJ'],
    'ENTP': ['INFJ', 'INTJ'],
    'ISFP': ['ENFJ', 'ESJF', 'ESTJ'],
    'ESFP': ['ISFJ', 'ISTJ'],
    'ISTP': ['ESFJ', 'ESTJ'],
    'ESTP': ['ISFJ', 'ISTJ'],
    'ISFJ': ['ESFP', 'ESTP'],
    'ESFJ': ['ISFP', 'ISTP'],
    'ISTJ': ['ESFP', 'ESTP'],
    'ESTJ': ['INTP', 'ISFP', 'ISTP'],
}


def get_today_date_string():
    today = datetime.today()

    return f'{today.year}-{today.month}-{today.day}'


class MbtiMatcher:

    @classmethod
    def get_matched_mbti_list(cls, mbti):
        return mbti_map[mbti]

    @classmethod
    def is_available_match(cls, user):
        from mbti.app import db
        today_string = get_today_date_string()

        today_match_log = db.match_log.find_one({
            'username': user.username,
            'date': today_string,
        })
        return today_match_log is None

    @classmethod
    def get_matched_user(cls, mbti_list, target_gender):
        from mbti.app import db

        inf = 987654321
        matched_user = {
            'view_count': inf,
        }

        for mbti in mbti_list:
            users = db.users.find({'mbti': mbti, 'gender': target_gender}, {'_id': False, 'password': False}).sort(
                'view_count', 1)

            for user in users:
                if matched_user['view_count'] > user['view_count']:
                    matched_user = user
                break

        if matched_user['view_count'] is not inf:
            return matched_user

    @classmethod
    def create_match_log(cls, user, matched_user):
        from mbti.app import db

        if matched_user is None:
            return

        today_string = get_today_date_string()

        db.match_log.insert_one({
            'username': user.username,
            'date': today_string,
        })

        db.users.update_one({'username': matched_user['username']},
                            {'$set': {'view_count': matched_user['view_count'] + 1}})

    @classmethod
    def match(cls, user):
        mbti = user.mbti
        mbti_list = cls.get_matched_mbti_list(mbti)
        opposite_gender = 'MALE' if user.gender is 'FEMALE' else 'FEMALE'
        matched_user = cls.get_matched_user(mbti_list, opposite_gender)
        cls.create_match_log(user, matched_user)

        return matched_user
