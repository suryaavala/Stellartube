from app import app
import flask_login

login_manager = flask_login.LoginManager()
login_manager.init_app(app)

class User(flask_login.UserMixin):
    
    def __init__(self, id):
        self.id = id
