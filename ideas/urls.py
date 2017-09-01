from django.conf.urls import url

from . import views

app_name = 'ideas'
urlpatterns = [
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<idea_id>[0-9]+)/$', views.detail, name='detail'),
]