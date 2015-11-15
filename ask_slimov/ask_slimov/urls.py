from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static

from ask_slimov import views, settings

urlpatterns = [
    url(r'^$',                          views.questions_new,        name = 'index'),
    url(r'^hot/?$',                     views.questions_hot,        name = 'hot'),
    url(r'^tag/(?P<tag>.+)/?$',         views.questions_tag,        name = 'tag'),
    url(r'^question/(?P<id>\d+)/?$',    views.question,             name = 'question'),
    url(r'^login/?$',                   views.form_login,           name = 'login'),
    url(r'^signup/?$',                  views.form_signup,          name = 'signup'),
    url(r'^ask/?$',                     views.form_question_new,    name = 'ask'),
    url(r'^admin/',                     include(admin.site.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
