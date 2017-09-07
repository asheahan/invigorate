from django.conf.urls import url

from . import views

app_name = 'ideas'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^new/$', views.NewIdeaView.as_view(), name='new'),
    url(r'^(?P<pk>[0-9]+)/edit/$', views.EditIdeaView.as_view(), name='edit'),
    url(r'^(?P<idea_id>[0-9]+)/$', views.detail, name='detail'),
]