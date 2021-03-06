"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from main import views as main
from django.views.generic.base import RedirectView
from django.conf.urls import url

urlpatterns = [
    path('', main.index),
    # path(r'^favicon\.ico$', RedirectView.as_view(url=r'static/favicon.ico')),
    path('admin/', admin.site.urls),
    path('hello/', main.test_post),
    path('cookie_craw/', main.cookie_crow),
    path('cookie_page/', main.cookie_homepage),
    path('verify/', main.verify_student),
    path('verify_homepage', main.verify_homepage),
    path('rank/', main.rank),
    path('ranking',main.ranking),
    path('rankinglm', main.rankinglm),
]
