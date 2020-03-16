from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flaskblog import db, login_manager
from flask_login import UserMixin


roles = ["Admin","blogger","superblogger","celebblogger","dev","Spec"]
myDict = {'Admin': 'Admin', 'us1': 'blogger', 'sus1': 'superblogger', 'celeb1': 'celebblogger', 
'us2': 'blogger', 'sus2': 'superblogger', 'celeb2': 'celebblogger', 'dev': 'dev'}
curr_user_id = None
curr_role = "Spec"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def add_role(user_name, role):
    myDict[user_name] = str(role)
    for key in myDict:
        print(key + " " + myDict[key] + " ")
    print(myDict)

def get_role(user_name):
    return myDict.get(user_name)

def get_curr_user_id():
    return curr_user_id
def update_curr_user_id(user_id):
    global curr_user_id
    curr_user_id = user_id

def set_curr_user(user_name):
    global curr_user_id, curr_role, myDict
    if(user_name == "logout"):
        curr_user_id = None
        curr_role = "Spec"
        return
    curr_user, = User.query.filter_by(username=user_name)
    print("In models.py: set_current_user " + str(curr_user))
    curr_user_id = curr_user.id
    curr_role = myDict.get(user_name)
    for key in myDict:
        print(key + " " + myDict[key] + " ")
    print("In models.py: set_current_user_id " +
          str(curr_user_id) + " role " + str(curr_role))
# def get_curr_user():
#     return curr_id


def get_precendence(role):
    print(role)
    if(role == roles[0]):
        print("Here1")
        return 100
    elif(role == roles[1]):
        print("Here2")
        return 1
    elif(role == roles[2]):
        print("Here3")
        return 2
    elif(role == roles[3]):
        print("Here4")
        return 3
    elif(role == roles[4]):
        print("Here5")
        return 99

def compare_precedence(role1, role2):
    if(role1 is None):
        print("Here6")
        return 0
    elif(role2 is None):
        print("Here7")
        return 0
    elif(role1 == role2):
        print("Here8")
        return 1
    elif(role1==100):
        print("Here9")
        return 1
    elif (role2 == 100):
        print("Here10")
        return 0
    elif (role1 > role2):
        print("Here11")
        return 0
    else:
        print("Here12")
        return 1

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


def get_post_role(cr_user_id):
    if(cr_user_id is None):
        return "Blogger"
    user = User.query.filter_by(id=cr_user_id).first()
    if(user is None):
        return "Blogger"    
    username = user.username
    print("In models.py: get_post_role " + str(user) +"user_id" + str(cr_user_id) + " username:" +str(myDict.get(username)))
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
    owners_role = db.Column(db.Integer, nullable = False, default = 0)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"