from django.shortcuts import render
from .models import whitePaper, wpClass, wpQuiz, userRole, wpTask
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.http import HttpResponseRedirect
from django.db.models import Q


# Create your views here.
def home(request):
    # print(request.user.userrole.role)  # Testing
    return render(request, 'task/homepage.html')


def wp_list(request):
    if request.user.is_authenticated:
        if request.user.userrole.role == 'EX':
            wplist = whitePaper.objects.filter(Q(accepted=False) | Q(acceptor=request.user))
        elif request.user.userrole.role == 'PO':
            wplist = whitePaper.objects.filter(uploader=request.user)
        elif request.user.userrole.role == 'AM':
            wplist = whitePaper.objects.filter(accepted=True)
        return render(request, 'task/whitepaperlist.html', {'wplist': wplist})
    else:
        return HttpResponseRedirect('/login/')


class wpForm(forms.ModelForm):
    dueTime = forms.DateField(label='Due Time', widget=forms.SelectDateWidget)
    class Meta:
        model = whitePaper
        fields = ['WPFile', 'title', 'description', 'dueTime']
        exclude = ('uploader',)


def upload_wp(request):
    if request.user.is_authenticated:
        if request.user.userrole.role == 'EX':
            wplist = whitePaper.objects.filter(Q(accepted=False) | Q(acceptor=request.user))
        elif request.user.userrole.role == 'PO':
            wplist = whitePaper.objects.filter(uploader=request.user)
        elif request.user.userrole.role == 'AM':
            wplist = whitePaper.objects.filter(accepted=True)
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
    if request.user.is_authenticated:
        if request.user.userrole.role == 'EX':
            wplist = whitePaper.objects.filter(Q(accepted=False) | Q(acceptor=request.user))
        elif request.user.userrole.role == 'PO':
            wplist = whitePaper.objects.filter(uploader=request.user)
        elif request.user.userrole.role == 'AM':
            wplist = whitePaper.objects.filter(accepted=True)
        old_file = whitePaper.objects.get(pk=wp_id)
        if old_file.uploader == request.user:
            if 'delete' in request.POST:
                old_file.delete()
                return HttpResponseRedirect('/wp_list/')
            elif 'update' in request.POST or 'upload' in request.POST:
                form = wpForm(request.POST or None, request.FILES, instance=old_file)
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect('/update_wp/'+wp_id)
                return render(request, 'task/upload_wp.html', {'form': form, 'wplist': wplist})
        elif not old_file.accepted and request.user.userrole.role == 'EX':
            if 'accept' in request.POST:
                old_file.accepted = True
                old_file.acceptor = request.user
                old_file.save()
                return HttpResponseRedirect('/update_wp/' + wp_id)

        return render(request, 'task/update_wp.html', {'old_file': old_file, 'wplist': wplist})
    else:
        return HttpResponseRedirect('/')


def class_list(request, wp_id):
    if request.user.is_authenticated:
        cl_list = wpClass.objects.filter(WP=whitePaper.objects.get(pk=wp_id))
        return render(request, 'task/classlist.html', {'cl_list': cl_list, 'wp_id': wp_id})
    else:
        return HttpResponseRedirect('/')


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
    if request.user.is_authenticated:
        cl_list = wpClass.objects.filter(WP=whitePaper.objects.get(pk=wp_id))
        old_class = wpClass.objects.get(pk=cl_id)
        if whitePaper.objects.get(pk=wp_id).acceptor == request.user:
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
        try:
            qz_list = wpQuiz.objects.get(WP=whitePaper.objects.get(pk=wp_id))
        except:
            qz_list = None
        return render(request, 'task/quizlist.html', {'qz_list': qz_list, 'wp_id': wp_id})
    else:
        return HttpResponseRedirect('/')


class wpQuizForm(forms.ModelForm):
    class Meta:
        model = wpQuiz
        exclude = ('WP',)


def upload_quiz(request, wp_id):
    if request.user.is_authenticated and whitePaper.objects.get(pk=wp_id).acceptor == request.user:
        if request.method == 'POST':
            form = wpQuizForm(request.POST)
            if form.is_valid():
                new_quiz = form.save(commit=False)
                new_quiz.WP = whitePaper.objects.get(pk=wp_id)
                form.save()
                return HttpResponseRedirect('/quiz_list/'+wp_id)
        else:
            form = wpQuizForm()
        return render(request, 'task/upload_quiz.html', {'form': form, 'wp_id': wp_id})
    else:
        return HttpResponseRedirect('/')


def update_quiz(request, wp_id):
    if request.user.is_authenticated and whitePaper.objects.get(pk=wp_id).acceptor == request.user:
        sel_quiz = wpQuiz.objects.get(WP=whitePaper.objects.get(pk=wp_id))
        form = wpQuizForm(request.POST or None, instance=sel_quiz)
        if request.method == 'POST':
            form.save()
            return HttpResponseRedirect('/quiz_list/'+wp_id)
        return render(request, 'task/upload_quiz.html', {'form': form, 'wp_id': wp_id})
    else:
        return  HttpResponseRedirect('/')


class ans1_sheet(forms.Form):
    ans1 = forms.CharField(max_length=1, widget=forms.Select(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')]))


class ans2_sheet(forms.Form):
    ans2 = forms.CharField(max_length=1, widget=forms.Select(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')]))


class ans3_sheet(forms.Form):
    ans3 = forms.CharField(max_length=1, widget=forms.Select(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')]))


class ans4_sheet(forms.Form):
    ans4 = forms.CharField(max_length=1, widget=forms.Select(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')]))


class ans5_sheet(forms.Form):
    ans5 = forms.CharField(max_length=1, widget=forms.Select(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4')]))


def take_quiz(request, wp_id):
    if request.user.is_authenticated:
        get_quiz = wpQuiz.objects.get(WP=whitePaper.objects.get(pk=wp_id))
        if request.method == 'POST':
            ans1 = ans1_sheet(request.POST)
            ans2 = ans2_sheet(request.POST)
            ans3 = ans3_sheet(request.POST)
            ans4 = ans4_sheet(request.POST)
            ans5 = ans5_sheet(request.POST)
            if ans1.is_valid() and ans2.is_valid() and ans3.is_valid() and ans4.is_valid() and ans5.is_valid():
                i = 0
                if ans1.cleaned_data['ans1'] == get_quiz.q1ans:
                    i += 1
                if ans2.cleaned_data['ans2'] == get_quiz.q2ans:
                    i += 1
                if ans3.cleaned_data['ans3'] == get_quiz.q3ans:
                    i += 1
                if ans4.cleaned_data['ans4'] == get_quiz.q4ans:
                    i += 1
                if ans5.cleaned_data['ans5'] == get_quiz.q5ans:
                    i += 1
                print(i)  # Number of correction
                return HttpResponseRedirect('/class_list/'+wp_id)
        ans1 = ans1_sheet()
        ans2 = ans2_sheet()
        ans3 = ans3_sheet()
        ans4 = ans4_sheet()
        ans5 = ans5_sheet()
        return render(request, 'task/quiz_page.html', {'get_quiz': get_quiz, 'ans1': ans1, 'ans2': ans2, 'ans3': ans3, 'ans4': ans4, 'ans5': ans5})
    else:
        return  HttpResponseRedirect('/')


def task_list(request, wp_id):
    if request.user.is_authenticated:
        if whitePaper.objects.get(pk=wp_id).uploader == request.user:
            t_list = wpTask.objects.filter(WP=whitePaper.objects.get(pk=wp_id))
        elif request.user.userrole.role == 'AM':
            t_list = wpTask.objects.filter(Q(WP=whitePaper.objects.get(pk=wp_id)) | Q(accepted=False))
        return render(request, 'task/task_list.html', {'t_list': t_list, 'wp_id': wp_id})
    else:
        return HttpResponseRedirect('/')


class wpTaskForm(forms.ModelForm):
    dueTime = forms.DateField(label='Due Time', widget=forms.SelectDateWidget)
    class Meta:
        model = wpTask
        fields = ['title', 'description', 'dueTime']
        exclude = ('WP',)


def upload_task(request, wp_id):
    if request.user.is_authenticated and whitePaper.objects.get(pk=wp_id).uploader == request.user:
        t_list = wpTask.objects.filter(WP=whitePaper.objects.get(pk=wp_id))
        if request.method == 'POST':
            form = wpTaskForm(request.POST)
            if form.is_valid():
                new_task = form.save(commit=False)
                new_task.WP = whitePaper.objects.get(pk=wp_id)
                form.save()
                return HttpResponseRedirect('/task_list/'+wp_id)
        else:
            form = wpTaskForm()
        return render(request, 'task/upload_task.html', {'form': form, 't_list': t_list, 'wp_id': wp_id})
    else:
        return HttpResponseRedirect('/')


def update_task(request, wp_id, t_id):
    if request.user.is_authenticated:
        if whitePaper.objects.get(pk=wp_id).uploader == request.user:
            t_list = wpTask.objects.filter(WP=whitePaper.objects.get(pk=wp_id))
        elif request.user.userrole.role == 'AM':
            t_list = wpTask.objects.filter(Q(WP=whitePaper.objects.get(pk=wp_id)) | Q(accepted=False))
        old_task = wpTask.objects.get(pk=t_id)
        if whitePaper.objects.get(pk=wp_id).uploader == request.user:
            if 'delete' in request.POST:
                old_task.delete()
                return HttpResponseRedirect('/task_list/'+wp_id)
            elif 'update' in request.POST or 'upload' in request.POST:
                form = wpTaskForm(request.POST or None, instance=old_task)
                if form.is_valid():
                    form.save()
                    return HttpResponseRedirect('/update_task/'+wp_id+'/'+t_id)
                return render(request, 'task/upload_task.html', {'form': form, 't_list': t_list, 'wp_id': wp_id})
        elif not old_task.accepted and request.user.userrole.role == 'AM':
            if 'accept' in request.POST:
                old_task.accepted = True
                old_task.acceptor = request.user
                old_task.save()
                return HttpResponseRedirect('/update_task/' + wp_id)

        return render(request, 'task/update_task.html', {'old_task': old_task, 't_list': t_list, 'wp_id': wp_id})
    else:
        return HttpResponseRedirect('/')


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
