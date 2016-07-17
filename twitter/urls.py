from django.conf.urls import url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url('^$', views.index,name='twitter_inicio'),
    url('^login/$', views.twitter_login),
    url('^register/$', views.register),
    url('^login/process/$', views.login_process),
    url('^logout/$', views.twitter_logout),
    url('^tweet/$', views.tweet),
    url('^page/(?P<page>\\d+)/$', views.index),
    url('^configuracion/$', views.conf,name='twitter_config'),
    url('^borrar/(?P<tweet_id>\\d+)/$', views.borrar),
    url('^profile/$', views.profile),
    url('^profile/page/(?P<page>\\d+)/$', views.profile),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)