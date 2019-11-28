from django.shortcuts import render
from .models import whitePaper, wpClass, wpQuiz, userRole
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.http import HttpResponseRedirect


# Create your views here.
def home(request):
    # print(request.user.userrole.role)  # Testing
    return render(request, 'task/homepage.html')


def wp_list(request):
    if request.user.is_authenticated:
        wplist = whitePaper.objects.all()
    return render(request, 'task/whitepaperlist.html', {'wplist': wplist})


class wpForm(forms.ModelForm):
    dueTime = forms.DateField(label='Due Time', widget=forms.SelectDateWidget)
    class Meta:
        model = whitePaper
        fields = ['WPFile', 'title', 'description', 'dueTime']
        exclude = ('uploader',)


def upload_wp(request):
    if request.user.is_authenticated:
        wplist = whitePaper.objects.all()
        if request.method == 'POST':
            form = wpForm(request.POST, request.FILES)
            if form.is_valid():
                new_wp = form.save(commit=False)
                new_wp.uploader = request.user
                form.save()
                return HttpResponseRedirect('/wp_list/')
        else:
            form = wpForm()
        return render(request, 'task/upload_wp.html', {'form': form, 'wplist': wplist})
    else:
        return HttpResponseRedirect('/login/')


def update_wp(request, wp_id):
    if request.user.is_authenticated and whitePaper.objects.get(pk=wp_id).uploader == request.user:
        wplist = whitePaper.objects.all()
        old_file = whitePaper.objects.get(pk=wp_id)
        if 'delete' in request.POST:
            old_file.delete()
            return HttpResponseRedirect('/wp_list/')
        elif 'update' in request.POST or 'upload' in request.POST:
            form = wpForm(request.POST or None, request.FILES, instance=old_file)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/update_wp/'+wp_id)
            return render(request, 'task/upload_wp.html', {'form': form, 'wplist': wplist})

        return render(request, 'task/update_wp.html', {'old_file': old_file, 'wplist': wplist})
    else:
        return HttpResponseRedirect('/')


def class_list(request, wp_id):
    if request.user.is_authenticated and whitePaper.objects.get(pk=wp_id).acceptor == request.user:
        cl_list = wpClass.objects.filter(WP=whitePaper.objects.get(pk=wp_id))
    return render(request, 'task/classlist.html', {'cl_list': cl_list, 'wp_id': wp_id})


class wpClassForm(forms.ModelForm):
    class Meta:
        model = wpClass
        field = ['video_url', 'title', 'description']
        exclude = ('WP',)


def upload_class(request, wp_id):
    if request.user.is_authenticated and whitePaper.objects.get(pk=wp_id).acceptor == request.user:
        cl_list = wpClass.objects.filter(WP=whitePaper.objects.get(pk=wp_id))
        if request.method == 'POST':
            form = wpClassForm(request.POST)
            if form.is_valid():
                new_class = form.save(commit=False)
                new_class.WP = whitePaper.objects.get(pk=wp_id)
                form.save()
                return HttpResponseRedirect('/class_list/'+wp_id)
        else:
            form = wpClassForm()
        return render(request, 'task/upload_class.html', {'form': form, 'cl_list': cl_list, 'wp_id': wp_id})
    else:
        return HttpResponseRedirect('/')


def update_class(request, wp_id, cl_id):
    if request.user.is_authenticated and whitePaper.objects.get(pk=wp_id).acceptor == request.user:
        cl_list = wpClass.objects.filter(WP=whitePaper.objects.get(pk=wp_id))
        old_class = wpClass.objects.get(pk=cl_id)
        if 'delete' in request.POST:
            old_class.delete()
            return HttpResponseRedirect('/class_list/'+wp_id)
        elif 'update' in request.POST or 'upload' in request.POST:
            form = wpClassForm(request.POST or None, instance=old_class)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/update_class/'+wp_id+'/'+cl_id)
            return render(request, 'task/upload_class.html', {'form': form, 'cl_list': cl_list, 'wp_id': wp_id})

        return render(request, 'task/update_class.html', {'old_class': old_class, 'cl_list': cl_list, 'wp_id': wp_id})
    else:
        return HttpResponseRedirect('/')


def quiz_list(request, wp_id):
    if request.user.is_authenticated and whitePaper.objects.get(pk=wp_id).acceptor == request.user:
        qz_list = wpQuiz.objects.filter(WP=whitePaper.objects.get(pk=wp_id))
    return render(request, 'task/quizlist.html', {'qz_list': qz_list, 'wp_id': wp_id})


class wpQuizForm(forms.ModelForm):
    CA = forms.CharField(label='Answer:', max_length=1, widget=forms.Select(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')]))
    class Meta:
        model = wpQuiz
        field = ['q1', 'a1', 'a2', 'a3', 'a4', 'CA']
        exclude = ('WP',)


def upload_quiz(request, wp_id):
    if request.user.is_authenticated and whitePaper.objects.get(pk=wp_id).acceptor == request.user:
        if request.method == 'POST':
            form = wpQuizForm(request.POST)
            if form.is_valid():
                new_quiz = form.save(commit=False)
                new_quiz.WP = whitePaper.objects.get(pk=wp_id)
                form.save()
                if 'next' in request.POST:
                    form = wpQuizForm()
                else:
                    return HttpResponseRedirect('/quiz_list/'+wp_id)
        else:
            form = wpQuizForm()
        return render(request, 'task/upload_quiz.html', {'form': form, 'wp_id': wp_id})
    else:
        return HttpResponseRedirect('/')


def take_quiz(request, wp_id):
    if request.user.is_authenticated:
        qz_list = wpQuiz.objects.filter(WP=whitePaper.objects.get(pk=wp_id))
        if request.method == 'POST':
            pass
        else:

            return render(request, 'task/quiz_page.html', {'qz_list': qz_list, 'ansSheet': ansSheet})

    else:
        return  HttpResponseRedirect('/')


def delete_quiz(request, wp_id, qz_id):
    if request.user.is_authenticated and whitePaper.objects.get(pk=wp_id).acceptor == request.user:
        sel_quiz = wpQuiz.objects.get(pk=qz_id)
        sel_quiz.delete()
        return HttpResponseRedirect('/quiz_list/'+wp_id)
    else:
        return  HttpResponseRedirect('/')


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
