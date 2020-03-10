from flask import render_template, request, Blueprint
from flaskblog.models import Post, get_curr_user_sec_level, get_post_sec_level, get_curr_user_id, set_curr_id, User
from sqlalchemy import join

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    print("POSSSST")
    if(get_curr_user_id() is None):
        page = request.args.get('page', 1, type=int)
        posts = Post.query.group_by(Post.id).having(Post.post_sec_level >= get_curr_user_sec_level()).order_by(Post.date_posted.desc())
        posts = posts.paginate(page=page, per_page=5)
        print("In If ")
        return render_template('home.html', posts=posts)
    else:
        print("In try")
        page = request.args.get('page', 1, type=int)
        posts = Post.query.group_by(Post.id).having(Post.post_sec_level >= get_curr_user_sec_level()).order_by(Post.date_posted.desc())
        print(posts)
        posts = posts.paginate(page=page, per_page=5)
        return render_template('home.html', posts=posts)


@main.route("/about")
def about():
    return render_template('about.html', title='About')
