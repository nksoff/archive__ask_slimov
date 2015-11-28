from ask_slimov.models import Tag
from django.contrib.auth.models import User
from ask_slimov.models import ProjectCache

# popular tags
def popular_tags(request):
    tags = ProjectCache.get_popular_tags()

    return {'popular_tags': tags}


# best users
def best_users(request):
    users = ProjectCache.get_best_users()

    return {'best_users': users}
