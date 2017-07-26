#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.conf.urls import url

from accounts.views import SignUpView, LoginView, LogOutView

urlpatterns = [
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^register/$', SignUpView.as_view(), name='signup'),
    url(r'^logout/$', LogOutView.as_view(), name='logout'),
]
