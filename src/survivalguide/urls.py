"""survivalguide URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from survivalguide.views import HomePageView, SignUpView, LoginView, LogOutView


urlpatterns = [
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^accounts/login/$', LoginView.as_view(), name='account_login'),
    url(r'^accounts/register/$', SignUpView.as_view(), name='account_signup'),
    url(r'^accounts/logout/$', LogOutView.as_view(), name='account_logout'),
    url(r'^talks/', include('talks.urls', namespace='talks')),
    url(r'^admin/', admin.site.urls),
]