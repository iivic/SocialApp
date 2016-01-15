"""social_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.http import HttpResponseRedirect
from django.conf import settings

urlpatterns = [
    #  Feed
    url(r'^$', lambda r: HttpResponseRedirect('feed/')),
    url(r'^feed/', include('feed.urls', namespace='posts')),
    #  Messenger
    url(r'^messenger/', include('messenger.urls', namespace='messages')),
    #  Authentication
    url(r'^admin/', include(admin.site.urls)),
    url('^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url('^logout/$', auth_views.logout, {'next_page': 'login'}, name='logout'),
    url(r'', include('registration.backends.simple.urls')),
    #  User Profile
    url(r'^profile/', include('user_details.urls', namespace='profile')),
]
if settings.DEBUG:
    urlpatterns.append(url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}))


