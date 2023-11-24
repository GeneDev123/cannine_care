from django.urls import path
from . import views

urlpatterns = [
  path('accounts/<str:login_or_register_param>/', views.user_login_and_register, name='login-register'),
  path('home/', views.home, name='home'),
  path('', views.home, name='home'),

  path('logout/', views.user_logout, name='logout'),
]