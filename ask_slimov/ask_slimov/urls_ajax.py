from django.conf.urls import include, url

from ask_slimov import views, settings

urlpatterns = [
    url(r'question/like/(?P<id>\d+)/?$',    views.ajax_question_like,       name = 'ajax_question_like'),
    url(r'answer/like/(?P<id>\d+)/?$',      views.ajax_answer_like,         name = 'ajax_answer_like'),
    url(r'answer/correct/(?P<id>\d+)/?$',   views.ajax_answer_correct,      name = 'ajax_answer_correct'),
]
