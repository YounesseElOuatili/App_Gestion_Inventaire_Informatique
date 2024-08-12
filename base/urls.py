from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.Dashboard, name='Dashboard'),
    re_path(r'login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', views.logout, name='logout'),

]
