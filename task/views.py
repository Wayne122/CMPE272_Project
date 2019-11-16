from django.shortcuts import render
from .models import whitePaper, videos, testQuestions, userRole
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.http import HttpResponseRedirect


# Create your views here.
def home(request):
    object_list = None
    if request.user.is_authenticated:
        object_list = whitePaper.objects.all()
        print(request.user.userrole.role)  # Testing
    return render(request, 'task/home.html', {'object_list': object_list})


class wpForm(forms.ModelForm):
    class Meta:
        model = whitePaper
        fields = ['WPFile', 'title', 'description', 'dueTime']
        exclude = ('uploader',)


def upload_wp(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = wpForm(request.POST, request.FILES)
            if form.is_valid():
                new_s3object = form.save(commit=False)
                new_s3object.owner = request.user
                form.save()
                return HttpResponseRedirect('/')
        else:
            form = wpForm()
        return render(request, 'task/upload_wp.html', {'form': form})
    else:
        return HttpResponseRedirect('/login/')


def update_wp(request, id):
    if request.user.is_authenticated and whitePaper.objects.get(pk=id).owner == request.user:
        old_file = whitePaper.objects.get(pk=id)
        form = wpForm(request.POST or None, request.FILES, instance=old_file)
        if request.POST and form.is_valid():
            form.save()
            return HttpResponseRedirect('/')

        return render(request, 'task/upload_wp.html', {'form': form})
    else:
        return HttpResponseRedirect('/login/')


def delete_wp(request, id):
    if request.user.is_authenticated and whitePaper.objects.get(pk=id).owner == request.user:
        sel_file = whitePaper.objects.get(pk=id)
        if request.method == 'POST':
            sel_file.delete()
            return HttpResponseRedirect('/')

        return render(request, 'task/delete_wp.html', {'sel_file': sel_file})
    else:
        return HttpResponseRedirect('/login/')


class registrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class userRoleForm(forms.ModelForm):
    role = forms.CharField(max_length=2, widget=forms.Select(choices=[('PO', 'Project Owner'), ('EX', 'Expert'), ('AM', 'Ambassador')]))
    class Meta:
        model = userRole
        fields = ['role']
        exclude = ['user']


def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    else:
        if request.method == 'POST':
            user_form = registrationForm(request.POST)
            user_role_form = userRoleForm(request.POST)
            if user_form.is_valid() and user_role_form.is_valid():
                new_user_role = user_role_form.save(commit=False)
                new_user = user_form.save()
                new_user_role.user = new_user
                user_role_form.save()
                return HttpResponseRedirect('/')
        else:
            user_form = registrationForm()
            user_role_form = userRoleForm()
        return render(request, 'task/registration/register.html', {'user_form': user_form, 'user_role_form': user_role_form})
