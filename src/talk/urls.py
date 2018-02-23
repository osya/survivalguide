from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from survivalguide.urls import ROUTER
from talk.views import TalkViewSet
from talklist.views import TalkListDeleteTalkView

app_name = 'talks'

ROUTER.register(r'talks', TalkViewSet, base_name='talk')

urlpatterns = [
    path('talk/<int:talklist_pk>/<int:pk>/delete/', TalkListDeleteTalkView.as_view(), name='delete_talk'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
