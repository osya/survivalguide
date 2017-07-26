from django.conf.urls import include, url
from . import views


list_patterns = [
    url(r'^$', views.TalkListListView.as_view(), name='list'),
    url(r'^d/(?P<slug>[-\w]+)/$', views.TalkListDetailView.as_view(), name='detail'),
    url(r'^create/$', views.TalkListCreateView.as_view(), name='create'),
    url(r'^e/(?P<slug>[-\w]+)/$', views.TalkListUpdateView.as_view(), name='update'),
    url(r'^s/(?P<slug>[-\w]+)/$', views.TalkListScheduleView.as_view(), name='schedult'),
    url(r'^delete/(?P<talk_list_pk>\d+)/(?P<pk>\d+)/$', views.TalkListDeleteTalkView.as_view(), name='delete_talk'),
]
urlpatterns = [
    url(r'^lists/', include(list_patterns, namespace='lists')),
]
