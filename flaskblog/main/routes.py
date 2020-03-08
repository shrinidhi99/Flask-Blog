from flask import render_template, request, Blueprint
from flaskblog.models import Post, get_curr_user, get_curr_user_sec_level, get_user_sec_level

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    print("POSSSST")
    page = request.args.get('page', 1, type=int)

    try:
        length, = Post.query.group_by(Post.id)
        posts = Post.query.group_by(Post.id).having(get_user_sec_level(Post.id) >= get_curr_user_sec_level()).order_by(Post.date_posted.desc())
        posts = posts.paginate(page=page, per_page=5)
        print("HAHASHDFKASLDFJASDF" + str(length))
        return render_template('home.html', posts=posts)
    except:
        posts = Post.query.order_by(Post.date_posted.desc())
        posts = posts.paginate(page=page, per_page=5)
        print("Empty")
        return render_template('home.html', posts=posts)

   


@main.route("/about")
def about():
    return render_template('about.html', title='About')