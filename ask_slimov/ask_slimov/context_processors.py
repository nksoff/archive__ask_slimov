from random import choice, shuffle

# popular tags
def popular_tags(request):
    tags = ['mysql', 'technopark', 'mail.ru', 'php', 'perl', 'ruby on rails', 'paraboloid', 'binary tree', 'css', 'json', 'cpp', 'binary-tree', 'bootstrap css', 'social network', 'c++11', ]
    colors = ['success', 'primary', 'default', 'danger', 'info']

    popular = [
            { 'tag': tag, 'color': choice(colors), } for tag in tags
    ]

    return {'popular_tags': popular}

# best users
def best_users(request):
    users = ['Mr. N', 'D. Medvedev', 'Ivan Smirnov', 'Domodedov Ilya', 'Sheremetyev Michael']
    shuffle(users)
    best = [
        { 'name': u } for u in users
    ]
    return {'best_users': best}
