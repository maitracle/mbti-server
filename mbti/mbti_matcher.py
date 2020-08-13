from datetime import datetime


mbti_map = {
    'INFP': ['ENFJ', 'ENTJ'],
    'ENFP': ['INFJ', 'INTJ'],
    'INFJ': ['ENTP', 'ENFP'],
    'ENFJ': ['INFP', 'ISFP'],
    'INTJ': ['ENTP', 'ENFP'],
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


def get_opposite_gender(gender):
    return 'MALE' if gender == 'FEMALE' else 'FEMALE'


class MbtiMatcher:

    @classmethod
    def get_matched_mbti_list(cls, mbti):
        return mbti_map[mbti]

    @classmethod
    def is_available_match(cls, user):
        from mbti.app import db
        today_string = get_today_date_string()

        today_match_log = db.match_log.find_one({
            'request_user': user.username,
            'date': today_string,
        })

        return today_match_log is None

    @classmethod
    def is_already_matched(cls, request_user, target_user):
        from mbti.app import db
        matched_log = db.match_log.find_one({
            request_user.gender: request_user.username,
            target_user['gender']: target_user['username'],
        })

        return matched_log is not None

    @classmethod
    def get_matched_user(cls, mbti_list, request_user, target_gender):
        from mbti.app import db

        inf = 987654321
        matched_user = {
            'view_count': inf,
        }

        for mbti in mbti_list:
            candidate_users = db.users.find({'mbti': mbti, 'gender': target_gender}, {'_id': False, 'password': False})\
                .sort('view_count', 1)

            for candidate in candidate_users:
                if cls.is_already_matched(request_user, candidate):
                    continue

                if matched_user['view_count'] > candidate['view_count']:
                    matched_user = candidate
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
            'request_user': user.username,
            user.gender: user.username,
            get_opposite_gender(user.gender): matched_user['username'],
            'date': today_string,
        })

        db.users.update_one({'username': matched_user['username']},
                            {'$set': {'view_count': matched_user['view_count'] + 1}})

    @classmethod
    def match(cls, user):
        mbti = user.mbti
        mbti_list = cls.get_matched_mbti_list(mbti)
        opposite_gender = get_opposite_gender(user.gender)
        matched_user = cls.get_matched_user(mbti_list, user, opposite_gender)
        cls.create_match_log(user, matched_user)

        return matched_user
