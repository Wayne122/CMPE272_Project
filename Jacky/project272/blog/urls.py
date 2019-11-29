from django.urls import path
from . import views
urlpatterns = [
    path('', views.homepage, name='homepage'),
    path('homepage', views.homepage, name='homepage'),
    path('whitepaperlistpage', views.whitepaperlist, name='whitepaperlist'),
    path('classpage', views.class_page, name='class_page'),
    path('managementpage', views.management_page, name='management_page'),
    path('classlistpage', views.classlist_page, name='classlist_page'),
    path('quizlistpage', views.quizlist_page, name='quizlist_page'),
    path('quizpage', views.quiz_page, name='quiz_page'),
    path('uploadclasspage', views.uploadclass_page, name='uploadclass_page'),
    path('updateclasspage', views.updateclass_page, name='updateclass_page'),
    path('createquizpage', views.createquiz_page, name='createquiz_page'),

    path('uploadwhitepage', views.uploadwhitepage_page, name='upload_page'),
    path('uppdatewhitepage', views.updatewhitepage_page, name='upload_page'),
]
