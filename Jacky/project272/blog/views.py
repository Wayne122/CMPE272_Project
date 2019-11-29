# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render

# Create your views here.
def homepage(request):
    return render(request, 'blog/homepage.html', {})

def whitepaperlist(request):
    return render(request, 'blog/whitepaperlist.html', {})

def class_page(request):
    if request.method == 'POST':
        uploaded_file = request.files['document']
        print(uploaded_file.name)
        print(uploaded_file.size)
        fs = FileSystemStorage()
        fs.save(uploaded_file.name, uploaded_file)
    return render(request, 'blog/class_page.html', {})

def management_page(request):
    return render(request, 'blog/management_page.html', {})

def uploadwhitepage_page(request):
    return render(request, 'blog/uploadwhite.html', {})

def updatewhitepage_page(request):
    return render(request, 'blog/updatewhite.html', {})

def classlist_page(request):
    return render(request, 'blog/classlist.html', {})

def quizlist_page(request):
    return render(request, 'blog/quizlist.html', {})

def quiz_page(request):
    return render(request, 'blog/quiz_page.html', {})

def uploadclass_page(request):
    return render(request, 'blog/upload_class.html', {})

def updateclass_page(request):
    return render(request, 'blog/update_class.html', {})

def createquiz_page(request):
    return render(request, 'blog/createquiz.html', {})
