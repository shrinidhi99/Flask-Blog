from flask import render_template, request, Blueprint
from flaskblog.models import Post, get_role, get_curr_user_id, get_curr_user_role, get_post_role

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.group_by(Post.id).having(get_post_role() >= get_curr_user_sec_level()).order_by(Post.date_posted.desc())
    posts = posts.paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)


@main.route("/about")
def about():
    return render_template('about.html', title='About')