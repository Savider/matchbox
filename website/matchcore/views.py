from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import JsonResponse

from .models import *
from .forms import *


def landing_page(request):
    context = []
    return render(request, 'matchcore/project_page.html', context)


def do_login(request):
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
        return redirect(login_page)


def login_page(request):
    form = LoginForm()
    context = {
        'form': form,
    }
    return render(request, 'matchcore/login_page.html', context)


def register_page(request):
    form = RegisterForm()
    context = {
        'form': form,
    }
    return render(request, 'matchcore/register_page.html', context)


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            img = form.cleaned_data['img']
            phone = form.cleaned_data['phone']
            discord = form.cleaned_data['discord']

            try:
                user = User.objects.create_user(username, email, password)
                person = Person.objects.create(user=user, img=img, phone=phone, discord=discord)
                login(request, user)
                return redirect(user_page, username=username)
            except:
                return redirect(login_page)
        else:
            redirect(register_page)
    else:
        return redirect(register_page)


def project_page(request, project_id):
    if request.user.is_authenticated:
        is_participant = False
        is_owner = False
        request_sent = False

        current_project = Project.objects.get(id=project_id)
        user = request.user
        project_participation = user.person.project_participations.filter(project__id=project_id).first()
        notif = Notification.objects.filter(sender=user.person, project=current_project, type="JR").first()

        if project_participation is not None:
            # is in this project
            is_participant = True
            if project_participation.owner:
                is_owner = True
            pass
        elif notif is not None:
            request_sent = True

        context = {
            'current_project': current_project,
            'request_sent': request_sent,
            'is_owner': is_owner,
            'is_participant': is_participant,
        }
        return render(request, 'matchcore/project_page.html', context)
    else:
        return redirect(login_page)


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


def notifications_page(request):
    if request.user.is_authenticated:
        # Show his notifications
        user = request.user
        notifications_received = user.person.received_notifications.all()
        read_notifications = notifications_received.filter(read=True)
        unread_notifications = notifications_received.filter(read=False)
        read_notifications = list(read_notifications)
        unread_notifications = list(unread_notifications)

        notifications_received.update(read=True)

        context = {
            'read_notifications': read_notifications,
            'unread_notifications': unread_notifications,
        }
        return render(request, 'matchcore/notifications_page.html', context)

    else:
        return redirect(login_page)


def filter_page(request):
    tags = ProjectTag.objects.all()
    context = {
        'tags': tags,
    }
    return render(request, 'matchcore/filter_page.html', context)


def find_page(request):

    # unfiltered page
    projects = Project.objects.filter(state='O')
    keys = list(request.GET.keys())
    if len(keys)>0:
        print("Here")
        tags = request.GET.keys()
        selected_projects = Project.objects.none()
        for t in tags:
            if request.GET[t] == 'on':
                selected_projects = selected_projects | Project.objects.filter(state='O').filter(tags__name=t)
        projects = selected_projects.distinct()


    context = {
        'projects': projects,
    }

    return render(request, 'matchcore/find_page.html', context)


def request_page(request, project_id):
    context = {
        'project_id': project_id,
    }
    return render(request, 'matchcore/request_page.html', context)


def join_request(request):

    project_id = request.POST.get('project_id')
    notif = Notification.objects.filter(type="JR").filter(project__id=project_id)
    if notif.count() > 0:
        # Already requested, do nothing
        return redirect(project_page, project_id=project_id)

    user = request.user
    project = Project.objects.get(id=project_id)
    owner = ProjectParticipation.objects.get(project=project, owner=True).person
    notif = Notification(sender=user.person, receiver=owner, project=project, type="JR")
    notif.save()

    return redirect(project_page, project_id=project_id)


def create_project_page(request):
    if request.user.is_authenticated:
        form = CreateProjectForm()
        context = {
            'form': form,
        }
        return render(request, 'matchcore/create_project_page.html', context)

    else:
        return redirect(login_page)


def create_project(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = CreateProjectForm(request.POST, request.FILES)
            if form.is_valid():
                title = form.cleaned_data['title']
                small_description = form.cleaned_data['small_description']
                big_description = form.cleaned_data['big_description']
                img = form.cleaned_data['img']
                complexity = form.cleaned_data['complexity']
                theme = form.cleaned_data['theme']
                technology = form.cleaned_data['technology']
                language = form.cleaned_data['language']

                tags = [ complexity , theme , technology , language]

                project = Project.objects.create(title=title, small_description=small_description,
                                                     big_description=big_description, img=img, state='O')
                project.tags.set(tags)
                project_participation = ProjectParticipation.objects.create(project=project,
                                                                                person=request.user.person, owner=True)
                return redirect(project_page, project_id=project.id)

            else:
                return redirect(login_page)

    else:
        return redirect(login_page)


def bzz(request):
    return render(request, 'matchcore/bzzzzzzz_deleteme.html')
