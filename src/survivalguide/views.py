#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class HomePageView(generic.TemplateView):
    template_name = 'home.html'


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    model = User
    template_name = 'accounts/signup.html'
