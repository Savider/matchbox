from django.contrib.auth.models import User
from django.db import models


class ProjectTag(models.Model):
    ARCHETYPE = [
        ('C', 'Complexity'),
        ('T', 'Theme'),
        ('D', 'Technology'),
        ('L', 'Language'),
    ]

    name = models.CharField(max_length=10)
    archetype = models.CharField(max_length=1, choices=ARCHETYPE, default='C')

    def __str__(self):
        return self.name


class UserTag(models.Model):
    name = models.CharField(max_length=10)
    img = models.ImageField(upload_to='images/tags')

    def __str__(self):
        return self.name


class Person(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='images/users', default='')
    nationality = models.CharField(max_length=20, default='Unknown')
    phone = models.CharField(max_length=10, default='None')
    discord = models.CharField(max_length=30, default='None')

    tags = models.ManyToManyField(UserTag)

    def __str__(self):
        return self.user.get_username()


class Project(models.Model):
    STATE = [
        ('O', 'Ongoing'),
        ('A', 'Archived'),
    ]

    title = models.CharField(max_length=50)
    small_description = models.CharField(max_length=100)
    big_description = models.CharField(max_length=1000)
    img = models.ImageField(upload_to='images/projects', default='')
    state = models.CharField(max_length=1, choices=STATE)

    tags = models.ManyToManyField(ProjectTag)
    participants = models.ManyToManyField(Person, through='ProjectParticipation')

    def __str__(self):
        return self.title


class ProjectParticipation(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='project_participations')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_participants')
    contribution = models.IntegerField(default=0)
    owner = models.BooleanField(default=False)


class Notification(models.Model):
    TYPE = [
        ('JR', 'Join Request'),
        ('RS', 'Request State'),
    ]

    sender = models.ForeignKey(Person, related_name='sent_notifications', on_delete=models.CASCADE)
    receiver = models.ForeignKey(Person, related_name='received_notifications', on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    type = models.CharField(max_length=2, choices=TYPE)
    read = models.BooleanField(default=False)
    accepted = models.BooleanField(default=False)
    interacted = models.BooleanField(default=False)
