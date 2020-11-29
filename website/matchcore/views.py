from django.shortcuts import render
from django.http import HttpResponse

from .models import Project


def project_page(request, project_id):
    response = "You're looking at project %s."
    return HttpResponse(response % project_id)


def project(request):
    project_list = Project.objects.all()
    output = ', '.join([p.title for p in project_list])
    return HttpResponse(output)
