from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flaskblog import db, login_manager
from flask_login import UserMixin


roles = {"Admin","Blogger","SuperBlogger","CelebBlogger","Dev","Spec"}
myDict = {"Admin":"Admin"}
curr_user_id = None
curr_role = "Spec"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def add_role(user_name, role):
    myDict[user_id] = str(role)
    print(myDict)

def get_role(user_name):
    return myDict.get(user_name)

def get_curr_user_id():
    return curr_user_id
def update_curr_user_id(user_id):
    global curr_user_id
    curr_user_id = user_id

def set_curr_user(user_name):
    global curr_user_id, curr_role
    if(user_name == "logout"):
        curr_id = None
        curr_role = "Spec"
        return
    curr_user, = User.query.filter_by(username=user_name)
    print("In models.py: set_current_user " + str(curr_user))
    curr_id = curr_user.id
    curr_role = myDict[user_name]
    print("In models.py: set_current_user_id " +
          str(curr_id) + "role " + str(curr_role))
# def get_curr_user():
#     return curr_id


def get_curr_user_role():
    global curr_user_id, curr_role
    print("In models.py: get_curr_user_role " +
          str(curr_user_id) + " role " + str(curr_role))
    if(curr_user_id == None):
        print("In models.py:role " + "Spec")
        return "Spec"
    else:
        print("In models.py get_curr_user_role: " + str(curr_role))
        return curr_role


def get_post_role(user_id):
    user = User.query.filter_by(id=user_id).first()
    username = user.username
    print("In models.py: get_post_role " + str(myDict.get(username)))
    return myDict.get(username)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"