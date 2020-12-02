from django.urls import path

from . import views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.login_page),
    path('project/', views.project),
    path('project/<int:project_id>/', views.project_page),
    path('user/<str:username>/', views.user_page),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
