
# chat/urls.py
from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<room_name>[^/]+)/(?P<user_name>[^/]+)/$', views.room, name='room'),
    url(r'^room_disconnect/$', views.room_disconnect, name='room_disconnect'),
]

