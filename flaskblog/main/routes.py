from flask import render_template, request, Blueprint
from flaskblog.models import Post, get_curr_user_sec_level, get_post_sec_level, get_curr_user_id, set_curr_id, User, user_id_list  # , num_of_user

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    print("POSSSST")
    page = request.args.get('page', 1, type=int)
    posts = Post.query.group_by(Post.id).having(1 > 0).order_by(
        Post.date_posted.desc())
    users = User.query.group_by(User.id).having(1 > 0)
    user_list = list(users)
    post_list = list(posts)
    num_of_user = len(user_list)
    print(post_list)
    print(user_list)
    print('Number of users = {}'.format(num_of_user))
    # Rows will include subjects and columns will include subjects and objects
    row_acm = []
    acm = []
    no_of_users = num_of_user
    no_of_posts = len(post_list)
    print('Number of posts = {}'.format(no_of_posts))

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
                    # print('Am here as user {}'.format(i))
                    row_acm.append([1, 0, 0, 0])
        acm.append(row_acm)
        # print(posts)
    user_obj = User()

    row_str = ''
    for i in range(num_of_user + no_of_posts + 1):
        if i == 0:
            row_str = row_str + '\t\t    admin\t'
        elif i <= num_of_user  and i != 0:
            user_obj = user_list[i - 1]
            row_str = row_str + '      ' + str(user_obj.username) + '      '
        else:
            row_str = row_str + '      ' + 'P' + str(i - num_of_user) + '     '

    print(row_str)
    # print('hey')
    for i in range(num_of_user + 1):
        if(i != 0):
            user_obj = user_list[i - 1]
            print(str(i) + '\t' + str(user_obj.username) + '\t' + str(acm[i]))
        else:
            print(str(i) + '\t' + 'admin' + '\t' + str(acm[i]))

    posts = posts.paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)


@main.route("/about")
def about():
    return render_template('about.html', title='About')
