from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^posts/(?P<pk>\d+)/$', views.show, name='show'),
    url(r'^posts/new/$', views.create, name='create'),
    url(r'^posts/like/$', views.like, name='like'),
    url(r'^posts/(?P<pk>\d+)/edit/$', views.update, name='update'),
    url(r'^posts/(?P<pk>\d+)/delete/$', views.delete, name='delete'),
    url(r'^comments/like/$', views.like_comment, name='like_comment'),
    url(r'^comments/(?P<pk>\d+)/delete/$', views.delete_comment, name='delete_comment'),
]
