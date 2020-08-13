import datetime

import bcrypt
from flask_jwt_extended import create_access_token


class User:
    def __init__(self, user_data):
        self.username = user_data['username']
        self.password = user_data['password']
        self.gender = user_data['gender']
        self.introduce = user_data['introduce']
        self.mbti = user_data['mbti']
        self.contact = user_data['contact']
        self.view_count = user_data['view_count']

    @classmethod
    def create_user(cls, user_data):
        from mbti.app import db

        if cls.is_exist_username(user_data['username']):
            raise ValueError('username이 중복되었습니다.')

        doc = {
            **user_data
        }
        encrypted_password = cls.get_encrypted_password(user_data['password'])
        doc['password'] = encrypted_password

        db.users.insert_one(doc)

    @classmethod
    def get_user_by_username(cls, username):
        from mbti.app import db

        if not cls.is_exist_username(username):
            raise ValueError('username가 존재하지 않습니다.')

        return cls(db.users.find_one({'username': username}, {'_id': False}))

    @staticmethod
    def get_encrypted_password(raw_password):
        password = bcrypt.hashpw(
            raw_password.encode('UTF-8'),
            bcrypt.gensalt()
        )

        return password

    @staticmethod
    def is_exist_username(username):
        from mbti.app import db

        return db.users.find_one({'username': username}) is not None

    @classmethod
    def is_valid_password(cls, username, password):
        from mbti.app import db
        hashed_password = db.users.find_one({'username': username})['password']
        is_valid = bcrypt.checkpw(password.encode('UTF-8'), hashed_password)

        return is_valid

    @classmethod
    def get_token(cls, username, password):
        if not cls.is_exist_username(username) or not cls.is_valid_password(username, password):
            return ''

        return create_access_token(identity=username, expires_delta=datetime.timedelta(days=1))
