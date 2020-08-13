

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

    @staticmethod
    def get_encrypted_password(raw_password):
        return raw_password

    @staticmethod
    def is_exist_username(username):
        from mbti.app import db

        return db.users.find_one({'username': username}) is not None

    @classmethod
    def is_valid_password(cls, username, password):
        return True

    @classmethod
    def get_token(cls, username, password):
        return 'asdf'
