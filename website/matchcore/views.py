from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.forms import formset_factory
from django.urls import reverse

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
    return render(request, 'matchcore/landing_page.html', context)


def register_page(request):
    form = RegisterForm()
    context = {
        'form': form,
    }
    return render(request, 'matchcore/register_page.html', context)


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            nationality = form.cleaned_data['nationality']
            img = form.cleaned_data['img']
            phone = form.cleaned_data['phone']
            discord = form.cleaned_data['discord']
            objective_tag = form.cleaned_data['objective_tag']
            expertise_tag = form.cleaned_data['expertise_tag']
            try:
                user = User.objects.create_user(username, email, password)
                person = Person.objects.create(user=user, img=img, nationality=nationality, phone=phone,
                                               discord=discord)
                person.tags.add(UserTag.objects.filter(name=objective_tag).first())
                person.tags.add(UserTag.objects.filter(name=expertise_tag).first())
                person.save()
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
        my_score = 0

        current_project = Project.objects.get(id=project_id)
        user = request.user
        project_participation = user.person.project_participations.filter(project__id=project_id).first()
        my_score = project_participation.contribution
        notif = Notification.objects.filter(sender=user.person, project=current_project, type="JR").first()

        if project_participation is not None:
            # is in this project
            my_score = project_participation.contribution
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
            'my_score': my_score,
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

    score = 0
    score_amount = 0
    for p in project_participations:
        if p.project.state == 'A' and p.owner is False:
            score += p.contribution
            score_amount = score_amount + 1

    if score_amount > 0:
        score = score / score_amount

    context = {
        'user': user,
        'current_projects': current_projects,
        'archived_projects': archived_projects,
        'score': score,
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
        read_notifications.reverse()
        unread_notifications.reverse()

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
    complexity_tags = ProjectTag.objects.filter(archetype='C')
    theme_tags = ProjectTag.objects.filter(archetype='T')
    technology_tags = ProjectTag.objects.filter(archetype='D')
    language_tags = ProjectTag.objects.filter(archetype='L')
    context = {
        'tags': tags,
        'complexity_tags': complexity_tags,
        'theme_tags': theme_tags,
        'technology_tags': technology_tags,
        'language_tags': language_tags,

    }
    return render(request, 'matchcore/filter_page.html', context)


def find_page(request):
    # unfiltered page
    projects = Project.objects.filter(state='O')
    keys = list(request.GET.keys())
    if len(keys) > 0:
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
    project = Project.objects.get(id=project_id)
    notif = Notification.objects.filter(type="JR").filter(project__id=project_id).filter(
        sender=request.user.person).first()
    requested = False
    if notif is not None:
        requested = True
    notif = Notification.objects.filter(type="RS").filter(project__id=project_id).filter(
        receiver=request.user.person).first()
    if notif is not None:
        requested = True
    context = {
        'project': project,
        'requested': requested,
    }
    return render(request, 'matchcore/request_page.html', context)


def join_request(request, project_id):
    notif = Notification.objects.filter(type="JR").filter(project__id=project_id).filter(sender=request.user.person)
    if notif.count() > 0:
        # Already requested, do nothing
        return redirect(request_page, project_id=project_id)

    user = request.user
    project = Project.objects.get(id=project_id)
    owner = ProjectParticipation.objects.get(project=project, owner=True).person
    notif = Notification(sender=user.person, receiver=owner, project=project, type="JR")
    notif.save()

    return redirect(request_page, project_id=project_id)


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

                tags = [complexity, theme, technology, language]

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


def profile_update_page(request):
    if request.user.is_authenticated:
        person = request.user.person
        form = ProfileUpdateForm(initial={
            'email': request.user.email,
            'img': person.img,
            'phone': person.phone,
            'nationality': person.nationality,
            'discord': person.discord
        })
        context = {
            'form': form,
        }
        return render(request, 'matchcore/user_settings.html', context)

    else:
        return redirect(login_page)


def profile_update(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            print(request)
            form = ProfileUpdateForm(request.POST, request.FILES)
            if form.is_valid():
                imgchanged = False
                if form.cleaned_data['img']:
                    imgchanged = True
                    img = form.cleaned_data['img']
                email = form.cleaned_data['email']
                nationality = form.cleaned_data['nationality']
                phone = form.cleaned_data['phone']
                discord = form.cleaned_data['discord']

                person = request.user.person
                request.user.email = email
                request.user.save()
                if imgchanged:
                    person.img = img
                person.nationality = nationality
                person.phone = phone
                person.discord = discord
                person.save()

                return redirect(user_page, username=request.user.username)

            else:
                return redirect(profile_update_page)
        else:
            return redirect(profile_update_page)
    else:
        return redirect(login_page)


def accept_request(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            notification_id = request.POST.get('notification_id')
            notification = Notification.objects.get(id=notification_id)
            notification.accepted = True
            notification.interacted = True
            new_notif = Notification(type='RS', project=notification.project, sender=notification.receiver,
                                     receiver=notification.sender, accepted=True)
            project_participation = ProjectParticipation(person=notification.sender, project=notification.project)

            notification.save()
            new_notif.save()
            project_participation.save()

            return redirect(notifications_page)
        else:
            return redirect(login_page)
    else:
        return redirect(login_page)


def reject_request(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            notification_id = request.POST.get('notification_id')
            notification = Notification.objects.get(id=notification_id)
            notification.accepted = False
            notification.interacted = True
            new_notif = Notification(type='RS', project=notification.project, sender=notification.receiver,
                                     receiver=notification.sender, accepted=False)

            notification.save()
            new_notif.save()

            return redirect(notifications_page)
        else:
            return redirect(login_page)
    else:
        return redirect(login_page)


def finish_project_page(request, project_id):
    project = Project.objects.filter(id=project_id)
    if request.user.is_authenticated:
        context = {}
        project_participations = ProjectParticipation.objects.filter(project__id=project_id, owner=False)
        num_participants = project_participations.count()

        # creating a formset
        EvaluateFormSet = formset_factory(EvaluateForm, extra=num_participants)
        formset = EvaluateFormSet()

        for form, participation in zip(formset, project_participations):
            form.fields['name'].initial = participation.person.user.username

        # Add the formset to context dictionary
        context['formset'] = formset
        context['project_id'] = project_id
        context['participations'] = project_participations

        return render(request, "matchcore/evaluate_page.html", context)
    else:
        return redirect(login_page)


def finish_project(request, project_id):
    if request.user.is_authenticated:
        if request.method == 'POST':
            EvaluateFormSet = formset_factory(EvaluateForm)
            formset = EvaluateFormSet(request.POST or None)
            for form in formset:
                if form.is_valid():
                    username = form.cleaned_data['name']
                    contribution = form.cleaned_data['contribution']
                    project_participation = ProjectParticipation.objects.get(project__id=project_id,
                                                                             person__user__username=username)
                    project_participation.contribution = contribution
                    project_participation.save()

            project = Project.objects.get(id=project_id)
            project.state = 'A'
            project.save()
            return redirect(user_page, username=request.user.username)
        else:
            return redirect(finish_project_page, project_id)
    else:
        return redirect(login_page)
