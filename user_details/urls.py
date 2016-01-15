from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.user_profile, name="user_info"),
    url(r'^change_password$', views.change_password, name="change_password"),
    url(r'^friends$', views.show_friends, name="show_friends"),
    url(r'^find_friends$', views.find_friends, name="find_friends"),
    url(r'^search_friends$', views.search_friends, name="search_friends"),
    url(r'^edit_friendship/$', views.edit_friendship, name="edit_friendship"),
]
