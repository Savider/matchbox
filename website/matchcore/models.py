from django.contrib.auth.base_user import AbstractBaseUser
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
    # img = models.CharField(max_length=100)  # Path
    img = models.ImageField(upload_to='images/tags')

    def __str__(self):
        return self.name


class User(AbstractBaseUser):
    username = models.CharField(max_length=16, unique=True)
    email = models.EmailField(unique=True)
    img = models.ImageField(upload_to='images/users', default='')
    phone = models.CharField(max_length=10, default='0')
    discord = models.CharField(max_length=30, default='None')

    tags = models.ManyToManyField(UserTag)

    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.get_username()


class Project(models.Model):
    STATE = [
        ('O', 'Ongoing'),
        ('A', 'Archived'),
    ]

    title = models.CharField(max_length=50)
    small_description = models.CharField(max_length=100)
    big_description = models.CharField(max_length=1000)
    img = models.CharField(max_length=100)  # Path
    state = models.CharField(max_length=1, choices=STATE)

    tags = models.ManyToManyField(ProjectTag)
    participants = models.ManyToManyField(User, through='ProjectParticipation')

    def __str__(self):
        return self.title


class ProjectParticipation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_participations')
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_participants')
    owner = models.BooleanField(default=False)


class Notification(models.Model):
    TYPE = [
        ('JR', 'Join Request'),
        ('RS', 'Request State'),
    ]

    sender = models.ForeignKey(User, related_name='sent_notifications', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_notifications', on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    type = models.CharField(max_length=2, choices=TYPE)
