#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from survivalguide.urls import ROUTER
from talklist.views import (TalkListCreateView, TalkListDetailView, TalkListListView, TalkListScheduleView,
                            TalkListUpdateView, TalkListViewSet)

app_name = 'talklists'

ROUTER.register(r'talk-lists', TalkListViewSet, base_name='talklist')

urlpatterns = [
    path('', TalkListListView.as_view(), name='list'),
    path('create/', TalkListCreateView.as_view(), name='create'),
    path('<slug:slug>/detail/', TalkListDetailView.as_view(), name='detail'),
    path('<slug:slug>/update/', TalkListUpdateView.as_view(), name='update'),
    path('<slug:slug>/schedule/', TalkListScheduleView.as_view(), name='schedule'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
