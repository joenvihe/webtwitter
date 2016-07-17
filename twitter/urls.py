from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^$', views.index,name='twitter_inicio'),
    url(r'^login/$', views.twitter_login),
    url(r'^register/$', views.register),
    url(r'^login/process/$', views.login_process),
    url(r'^logout/$', views.twitter_logout),
    url(r'^tweet/$', views.tweet),
    url(r'^page/(?P<page>\\d+)/$', views.index),
    url(r'^configuracion/$', views.conf,name='twitter_config'),
    url(r'^borrar/(?P<tweet_id>\\d+)/$', views.borrar),
    url(r'^profile/$', views.profile),
    url(r'^profile/page/(?P<page>\\d+)/$', views.profile),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)