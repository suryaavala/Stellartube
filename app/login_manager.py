from flask_login import UserMixin
from app import database as db

class User(UserMixin):
    
    def __init__(self, userid):
        self.id = userid
        self.username = db.sql_GetUsernameByUserID(userid)

    def get_username(self):
        return self.username
