# Discretionary Access Control


class Post(object):
    def __init__(self, post_id, user_id, content, date_posted, title):
        self.post_id = post_id
        self.user_id = user_id
        self.content = content
        self.date_posted = date_posted
        self.title = title


posts = []

# Rows will include subjects and columns will include subjects and objects
row_acm = []
acm = []
no_of_users = 4
no_of_posts = 2

for i in range(no_of_users + 1):
    global row_acm = []
    for j in range(no_of_users + no_of_posts + 1):
        if i == 0:
            row_acm.append([1, 1, 1, 1])
        else:
            if j == i:
                row_acm.append([1, 1, 1, 1])
            elif j == 0 and i != 0: # no other subject has an access on admin
                row_acm.append([0, 0, 0, 0])
            elif (j > i) and (j >= no_of_users + 1) and (i == posts[j-no_of_users-1].user_id):
                row_acm.append([1, 1, 1, 1])
            elif i != j and j <= no_of_users: # a subject doesn't have an access over any other subject
                row_acm.append([0, 0, 0, 0])
            else:
                print('Am here as user {}'.format(i))
                row_acm.append([1, 0, 0, 0])
    acm.append(row_acm)

for i in range(no_of_users + 1):
    print(acm[i])

def checkRead(post_id, user_id):
    if acm[user_id][no_of_users+1+post_id]==[1,0,0,0]:
        return 1
    else:
        return 0
