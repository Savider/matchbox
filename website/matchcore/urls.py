from django.urls import path

from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.login_page),
    path('login/submit', views.do_login),

    path('register', views.register_page),
    path('register/submit', views.register),

    path('project/<int:project_id>/', views.project_page),

    path('user/<str:username>/', views.user_page),

    path('notifications', views.notifications_page),

    path('filter', views.filter_page),

    path('find', views.find_page),

    path('notifications/', views.notifications_page),

    path('request_page/<int:project_id>/', views.request_page),
    path('join_request', views.join_request),

    path('create_project', views.create_project_page),
    path('create_project/submit', views.create_project),

    path('bzz/', views.bzz)
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
