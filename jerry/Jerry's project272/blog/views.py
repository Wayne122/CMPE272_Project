# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render

# Create your views here.
def homepage(request):
    return render(request, 'blog/management_page.html', {})

def second_page(request):
    return render(request, 'blog/second_page.html', {})

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
