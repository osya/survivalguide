from django.conf.urls import include, url
from . import views


list_patterns = [
    url(r'^$', views.TalkListListView.as_view(), name='list'),
    url(r'^d/(?P<slug>[-\w]+)/$', views.TalkListDetailView.as_view(), name='detail'),
    url(r'^create/$', views.TalkListCreateView.as_view(), name='create'),
]
urlpatterns = [
    url(r'^lists/', include(list_patterns, namespace='lists')),
]
