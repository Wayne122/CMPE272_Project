from django.urls import path
from . import views
urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('', views.second_page, name='second_page'),
    path('', views.class_page, name='class_page'),
    path('', views.management_page, name='management_page'),
]
