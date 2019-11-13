"""CMPE272_Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.conf.urls import include, re_path
from django.contrib.auth import views as auth_views

from task.views import home, register, upload_wp, update_wp, delete_wp

urlpatterns = [
    re_path(r'^admin/', admin.site.urls),
    re_path(r'^$', home, name='home'),
    re_path(r'^login/$', auth_views.LoginView.as_view(template_name='task/registration/login.html'), name='login'),
    re_path(r'^logout/$', auth_views.LogoutView.as_view(), name='logout'),
    re_path(r'^register/$', register, name='register'),

    re_path(r'^upload_wp/$', upload_wp, name='upload_wp'),
    re_path(r'^update_wp/(?P<id>[\w-]+)/$', update_wp, name='update_wp'),
    re_path(r'^delete_wp/(?P<id>[\w-]+)/$', delete_wp, name='delete_wp'),
]
