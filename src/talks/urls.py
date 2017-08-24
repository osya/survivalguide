from django.conf.urls import include, url

from talks.views import TalkListListView, TalkListDetailView, TalkListCreateView, TalkListUpdateView, \
    TalkListScheduleView, TalkListDeleteTalkView, TalkListListApi, TalkListDetailApi, TalkDetailApi

list_api_patterns = [
    url(r'^$', TalkListListApi.as_view(), name='list'),
    url(r'^(?P<pk>\d+)/$', TalkListDetailApi.as_view(), name='detail'),
]

api_patterns = [
    url(r'^(?P<pk>\d+)/$', TalkDetailApi.as_view(), name='detail'),
]

list_patterns = [
    url(r'^$', TalkListListView.as_view(), name='list'),
    url(r'^api/', include(list_api_patterns, namespace='api')),
    url(r'^create/$', TalkListCreateView.as_view(), name='create'),
    url(r'^(?P<slug>[-\w]+)/detail/$', TalkListDetailView.as_view(), name='detail'),
    url(r'^(?P<slug>[-\w]+)/update/$', TalkListUpdateView.as_view(), name='update'),
    url(r'^(?P<slug>[-\w]+)/schedule/$', TalkListScheduleView.as_view(), name='schedule'),
]
urlpatterns = [
    url(r'^api/', include(api_patterns, namespace='api')),
    url(r'^talk_lists/', include(list_patterns, namespace='talk_lists')),
    url(r'^talk/(?P<talk_list_pk>\d+)/(?P<pk>\d+)/delete/$', TalkListDeleteTalkView.as_view(), name='delete_talk'),
]
