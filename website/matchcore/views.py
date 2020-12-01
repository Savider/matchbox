from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import HttpResponse

from .models import *
from .forms import *


def landing_page(request):
    context = []
    return render(request, 'matchcore/project_page.html', context)


def login_page(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect(user_page, username=username)
            else:
                return redirect(login_page)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = LoginForm()
        context = {
            'form': form,
        }
        return render(request, 'matchcore/login_page.html', context)


def project_page(request, project_id):
    current_project = Project.objects.get(id=project_id)
    context = {
        'current_project': current_project,
    }
    return render(request, 'matchcore/project_page.html', context)


def user_page(request, username):
    user = User.objects.get(username=username)
    project_participations = user.person.project_participations.all()
    projects = [p.project for p in project_participations]
    current_projects = []
    archived_projects = []
    for p in projects:
        if p.state == 'O':
            current_projects.append(p)
        else:
            archived_projects.append(p)

    context = {
        'user': user,
        'current_projects': current_projects,
        'archived_projects': archived_projects,
    }
    return render(request, 'matchcore/user_page.html', context)


def project(request):
    project_list = Project.objects.all()
    output = ', '.join([p.id.__str__() for p in project_list])
    return HttpResponse(output)
