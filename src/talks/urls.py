from django.conf.urls import include, url
from rest_framework.routers import DefaultRouter
from rest_framework.urlpatterns import format_suffix_patterns

from talks.views import (TalkListCreateView, TalkListDeleteTalkView, TalkListDetailView, TalkListListView,
                         TalkListScheduleView, TalkListUpdateView, TalkListViewSet, TalkViewSet)

router = DefaultRouter()
router.register(r'talk-lists', TalkListViewSet, base_name='talk_list')
router.register(r'talks', TalkViewSet, base_name='talk')

list_patterns = [
    url(r'^$', TalkListListView.as_view(), name='list'),
    url(r'^create/$', TalkListCreateView.as_view(), name='create'),
    url(r'^(?P<slug>[-\w]+)/detail/$', TalkListDetailView.as_view(), name='detail'),
    url(r'^(?P<slug>[-\w]+)/update/$', TalkListUpdateView.as_view(), name='update'),
    url(r'^(?P<slug>[-\w]+)/schedule/$', TalkListScheduleView.as_view(), name='schedule'),
]
urlpatterns = [
    url(r'^talk-list/', include(list_patterns, namespace='talk_lists')),
    url(r'^talk/(?P<talk_list_pk>\d+)/(?P<pk>\d+)/delete/$', TalkListDeleteTalkView.as_view(), name='delete_talk'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
