from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static

from ask_slimov import views, settings, urls_ajax

urlpatterns = [
                  url(r'^$', views.questions_new, name='index'),
                  url(r'^hot/?$', views.questions_hot, name='hot'),
                  url(r'^tag/(?P<tag>.+)/?$', views.questions_tag, name='tag'),
                  url(r'^question/(?P<id>\d+)/?$',
                      views.question,
                      name='question'),
                  url(r'^login/?$', views.form_login, name='login'),
                  url(r'^logout/?$', views.logout, name='logout'),
                  url(r'^signup/?$', views.form_signup, name='signup'),
                  url(r'^ask/?$', views.form_question_new, name='ask'),
                  url(r'^profile/edit/?$',
                      views.form_profile_edit,
                      name='profile_edit'),
                  url(r'^admin/', include(admin.site.urls)),
                  url(r'^ajax/', include(urls_ajax)),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
