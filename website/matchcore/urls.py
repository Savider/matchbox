from django.urls import path

from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.login_page),
    path('login/submit', views.do_login),

    path('register', views.register_page, name="register"),
    path('register/submit', views.register),

    path('project/<int:project_id>/', views.project_page, name="project_page"),

    path('user/<str:username>/', views.user_page, name="user_page"),

    path('notifications/', views.notifications_page, name="notifications"),

    path('filter', views.filter_page, name="filter_page"),

    path('find', views.find_page, name="find_page"),

    path('request_page/<int:project_id>/', views.request_page, name="request_page"),
    path('request_page/<int:project_id>/submit', views.join_request),

    path('accept_request', views.accept_request),
    path('reject_request', views.reject_request),

    path('create_project', views.create_project_page, name="create_project"),
    path('create_project/submit', views.create_project),

    path('profile_update', views.profile_update_page, name="profile_update"),
    path('profile_update/submit', views.profile_update),

    path('evaluate/<int:project_id>/', views.finish_project_page, name="finish_project"),
    path('evaluate/<int:project_id>/submit', views.finish_project),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
