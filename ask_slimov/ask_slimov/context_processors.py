from ask_slimov.models import Tag
from django.contrib.auth.models import User


# popular tags
def popular_tags(request):
    tags = Tag.objects.order_by_question_count().all()[:12]

    return {'popular_tags': tags}


# best users
def best_users(request):
    users = User.objects.all()[0:10] 

    return {'best_users': users}
