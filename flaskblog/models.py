from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flaskblog import db, login_manager
from flask_login import UserMixin


curr_user = None
curr_id = None
curr_sec_level = None
user_id_list = [1]
num_of_user = 0


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def add_user_id():
    max_user_id = user_id_list[len(user_id_list)-1]
    user_id_list.append(max_user_id+1)

def inc_num_of_user():
    global num_of_user
    num_of_user= num_of_user+1

def set_curr_user(user_name):
    global curr_id, curr_sec_level
    if(user_name == "logout"):
        curr_id = None
        curr_sec_level = 5
        return
    curr_user, = User.query.filter_by(username=user_name)
    print("In models.py: set_current_user " + str(curr_user))
    curr_id = curr_user.id
    curr_sec_level = curr_user.sec_level
    print("In models.py: set_current_user_id " +
          str(curr_id) + "sec_level " + str(curr_sec_level))
# def get_curr_user():
#     return curr_id


def get_curr_user_sec_level():
    global curr_id, curr_sec_level
    print("In models.py: get_curr_user_sec_level " +
          str(curr_id) + " sec_level " + str(curr_sec_level))
    if(curr_id == None):
        print("In models.py:sec_level " + str(5))
        return 5
    else:
        print("In models.py curr_sec_level: " + str(curr_sec_level))
        return curr_sec_level


def get_post_sec_level(user_id):
    user = User.query.filter_by(id=user_id).first()
    print("In models.py: get_post_sec_level:user " + str(user))
    print("In models.py: get_post_sec_level:user_id " + user_id)
    sec_level = user.sec_level
    print("In models.py: get_post_sec_level " + str(sec_level))
    return sec_level


def get_curr_user_id():
    global curr_id
    return curr_id


def set_curr_id(user_id):
    global curr_id
    curr_id = user_id


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    sec_level = db.Column(db.Integer, nullable=False, default=1)
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
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # sec_level = User.query.filter_by(id = user_id)
    # curr_owner_of_post, = User.query.filter_by(id = user_id)
    # print("Post Sec owner " +str(curr_owner_of_post))
    # sec_level = curr_owner_of_post.sec_level
    # print("Post Sec Level " +str(sec_level))

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
