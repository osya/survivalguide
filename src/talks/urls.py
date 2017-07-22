from django.conf.urls import include, url
from . import views


list_patterns = [
    url(r'^$', views.TalkListListView.as_view(), name='list'),
    url(r'^/(?P<slug>[-\w]+)/$', views.TalkListDetailView.as_view(), name='detail'),
]
urlpatterns = [
    url(r'^lists/', include(list_patterns, namespace='lists')),
]
