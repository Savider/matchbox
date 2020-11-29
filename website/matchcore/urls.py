from django.urls import path

from . import views

urlpatterns = [
    path('project/', views.project, name='project'),
    path('project/<int:project_id>/', views.project_page, name='project_page'),
]