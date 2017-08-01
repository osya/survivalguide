from django.conf.urls import include, url
from . import views


list_patterns = [
    url(r'^$', views.TalkListListView.as_view(), name='list'),
    url(r'^(?P<slug>[-\w]+)/detail/$', views.TalkListDetailView.as_view(), name='detail'),
    url(r'^create/$', views.TalkListCreateView.as_view(), name='create'),
    url(r'^(?P<slug>[-\w]+)/update/$', views.TalkListUpdateView.as_view(), name='update'),
    url(r'^(?P<slug>[-\w]+)/schedule/$', views.TalkListScheduleView.as_view(), name='schedule'),
]
urlpatterns = [
    url(r'^talklist/', include(list_patterns, namespace='talklist')),
    url(r'^talk/(?P<talk_list_pk>\d+)/(?P<pk>\d+)/delete/$', views.TalkListDeleteTalkView.as_view(), name='delete_talk'),
]
