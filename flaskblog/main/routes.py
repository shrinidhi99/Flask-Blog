from flask import render_template, request, Blueprint
from flaskblog.models import Post, get_curr_user_sec_level, get_post_sec_level, get_curr_user_id, set_curr_id, User, user_id_list, num_of_user

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    print("POSSSST")
    page = request.args.get('page', 1, type=int)
    posts = Post.query.group_by(Post.id).having(1 > 0).order_by(
        Post.date_posted.desc())
    # users = User.query.group_by(User.id).having(1>0)
    post_list = list(posts)
    # Rows will include subjects and columns will include subjects and objects
    row_acm = []
    acm = []
    no_of_users = num_of_user
    no_of_posts = len(post_list)

    for i in range(no_of_users + 1):
        row_acm = []
        for j in range(no_of_users + no_of_posts + 1):
            if i == 0:
                row_acm.append([1, 1, 1, 1])
            else:
                if j == i:
                    row_acm.append([1, 1, 1, 1])
                elif j == 0 and i != 0:  # no other subject has an access on admin
                    row_acm.append([0, 0, 0, 0])
                elif (j > i) and (j >= no_of_users + 1) and (
                        i == posts[j - no_of_users - 1].user_id):
                    row_acm.append([1, 1, 1, 1])
                elif i != j and j <= no_of_users:  # a subject doesn't have an access over any other subject
                    row_acm.append([0, 0, 0, 0])
                else:
                    print('Am here as user {}'.format(i))
                    row_acm.append([1, 0, 0, 0])
        acm.append(row_acm)
        # print(posts)
    posts = posts.paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)


@main.route("/about")
def about():
    return render_template('about.html', title='About')
