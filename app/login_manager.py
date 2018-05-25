import flask_login as fl
from app import database as db
from app import app
from app import stellar_block as sb

# User class for storing current user related data for current session
class User(fl.UserMixin):
    
    def __init__(self, userid):
        self.id = userid
        
        user_info = db.sql_getAllUserInfo(userid)
        self.email = user_info[0]
        self.fname = user_info[1]
        self.lname = user_info[2]
        

        bc = sb.Stellar_block(user_info[3])
        self.balance = bc._get_balance()

    def get(userid):
        return User(userid) if db.sql_getUser(userid) else None


# Initialise login session manager
lm = fl.LoginManager()
lm.init_app(app)

@lm.user_loader
def load_user(userid):
    return User.get(userid)
