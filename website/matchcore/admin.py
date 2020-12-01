from django.contrib import admin

from .models import *

admin.site.register(Project)
admin.site.register(ProjectTag)
admin.site.register(ProjectParticipation)
admin.site.register(Person)
admin.site.register(UserTag)
admin.site.register(Notification)
