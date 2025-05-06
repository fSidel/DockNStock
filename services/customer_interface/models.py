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
    
    