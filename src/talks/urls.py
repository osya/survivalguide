from django.conf.urls import include, url

from talks.views import TalkListListView, TalkListDetailView, TalkListCreateView, TalkListUpdateView, \
    TalkListScheduleView, TalkListDeleteTalkView

list_patterns = [
    url(r'^$', TalkListListView.as_view(), name='list'),
    url(r'^(?P<slug>[-\w]+)/detail/$', TalkListDetailView.as_view(), name='detail'),
    url(r'^create/$', TalkListCreateView.as_view(), name='create'),
    url(r'^(?P<slug>[-\w]+)/update/$', TalkListUpdateView.as_view(), name='update'),
    url(r'^(?P<slug>[-\w]+)/schedule/$', TalkListScheduleView.as_view(), name='schedule'),
]
urlpatterns = [
    url(r'^talklist/', include(list_patterns, namespace='talklist')),
    url(r'^talk/(?P<talk_list_pk>\d+)/(?P<pk>\d+)/delete/$', TalkListDeleteTalkView.as_view(), name='delete_talk'),
]
