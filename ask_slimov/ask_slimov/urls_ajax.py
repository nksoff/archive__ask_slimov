from django.conf.urls import url

from ask_slimov import views

urlpatterns = [
    url(r'question/like/(?P<id>\d+)/?$',
        views.AjaxQuestionLike.as_view(),
        name='ajax_question_like'),
    url(r'answer/like/(?P<id>\d+)/?$',
        views.AjaxAnswerLike.as_view(),
        name='ajax_answer_like'),
    url(r'answer/correct/(?P<id>\d+)/?$',
        views.AjaxAnswerCorrect.as_view(),
        name='ajax_answer_correct'),
    url(r'question/answers/(?P<id>\d+)/(?P<page>\d+)/?$',
        views.AjaxQuestionAnswers.as_view(),
        name='ajax_question_answers'),
    url(r'question/answer/add/(?P<id>\d+)/?$',
        views.AjaxAnswerAdd.as_view(),
        name='ajax_question_answer_add'),
]
