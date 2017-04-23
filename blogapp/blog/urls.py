# -*- coding: utf-8 -*-
from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.post_list),
    url(r'^post/(?P<pk>[0-9]+)/edit/$', views.post_edit, name='post_edit'),
    url(r'^post/(?P<pk>[0-9]+)/edit/key_check/$', views.key_check_edit, name='key_check_edit'),
    url(r'^post/(?P<pk>[0-9]+)/details/$', views.post_detail, name='post_detail'),
    url(r'^post/(?P<pk>[0-9]+)/key_check/$', views.key_check, name='key_check'),
    url(r'^post/(?P<pk>[0-9]+)/delete/$', views.post_delete, name='post_delete'),
    url(r'^post/new/$', views.post_new, name='post_new'),
]