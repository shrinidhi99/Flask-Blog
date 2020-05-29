from flask import render_template, request, Blueprint
from flaskblog.models import Post, get_role, get_curr_user_id, getTopicofMod, get_curr_user_role, get_post_role,get_curr_user_name, get_precendence, get_role, compare_precedence

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    
        
    page = request.args.get('page', 1, type=int)
    if(get_curr_user_role()=='moderator'):
        posts = Post.query.group_by(Post.id).having(Post.topic == getTopicofMod(get_curr_user_name())).order_by(Post.date_posted.desc())
    else:
        posts = Post.query.group_by(Post.id).having(Post.owners_role >= get_precendence(get_curr_user_role())).order_by(Post.date_posted.desc())
    posts = posts.paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)


@main.route("/about")
def about():
    return render_template('about.html', title='About')