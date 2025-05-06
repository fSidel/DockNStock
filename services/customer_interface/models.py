from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from config import Config

class User(UserMixin):
    def __init__(self, id, username):
        self.id = id
        self.username = username

    def to_dict(self):
        """Convert the User object to a dictionary."""
        return {"id": self.id, "username": self.username}
    
    def get_reset_token(self, expires_sec=1800):
        s = Serializer(Config.SECRET_KEY, expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(Config.SECRET_KEY)
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)