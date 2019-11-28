from django.urls import path
from . import views
urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('homepage', views.homepage, name='homepage'),
    path('secondpage', views.second_page, name='second_page'),
    path('classpage', views.class_page, name='class_page'),
    path('managementpage', views.management_page, name='management_page'),
]
