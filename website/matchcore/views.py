from django.shortcuts import render
from django.http import HttpResponse

from .models import *


def project_page(request, project_id):
    current_project = Project.objects.get(id=project_id)
    context = {
        'current_project': current_project,
    }
    return render(request, 'matchcore/project_page.html', context)


def user_page(request, username):
    user = User.objects.get(username=username)
    project_participations = user.project_participations.all()
    projects = [p.project for p in project_participations]
    context = {
        'user': user,
        'projects': projects,
    }
    return render(request, 'matchcore/user_page.html', context)


def project(request):
    project_list = Project.objects.all()
    output = ', '.join([p.id.__str__() for p in project_list])
    return HttpResponse(output)
