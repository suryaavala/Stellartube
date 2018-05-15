import flask_login as fl
from app import database as db
from app import app

# User class for storing current user related data for current session
class User(fl.UserMixin):
    
    def __init__(self, userid):
        self.id = userid
        self.email, self.fname, self.lname = db.sql_getUser(userid)


# Initialise login session manager
lm = fl.LoginManager()
lm.init_app(app)

@lm.user_loader
def load_user(userid):
    return User(userid)
