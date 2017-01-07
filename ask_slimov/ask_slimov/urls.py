from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.static import static

from ask_slimov import views, settings, urls_ajax

urlpatterns = [
                  url(r'^$', views.QuestionsNew.as_view(), name='index'),
                  url(r'^hot/?$', views.QuestionsHot.as_view(), name='hot'),
                  url(r'^tag/(?P<tag>.+)/?$',
                      views.QuestionsTag.as_view(),
                      name='tag'),
                  url(r'^question/(?P<id>\d+)/?$',
                      views.SingleQuestion.as_view(),
                      name='question'),
                  url(r'^login/?$', views.Login.as_view(), name='login'),
                  url(r'^logout/?$', views.Logout.as_view(), name='logout'),
                  url(r'^signup/?$', views.Signup.as_view(), name='signup'),
                  url(r'^ask/?$', views.QuestionNew.as_view(), name='ask'),
                  url(r'^profile/edit/?$',
                      views.ProfileEdit.as_view(),
                      name='profile_edit'),
                  url(r'^admin/', include(admin.site.urls)),
                  url(r'^ajax/', include(urls_ajax)),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
