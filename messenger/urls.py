from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^conversations/(?P<pk>\d+)/$', views.show, name='show'),
    url(r'^conversations/new/$', views.create, name='create'),
    url(r'^conversations/(?P<pk>\d+)/delete/$', views.delete, name='delete'),
]
