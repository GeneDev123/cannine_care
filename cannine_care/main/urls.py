from django.urls import path
from . import views

urlpatterns = [
  path('accounts/<str:login_or_register_param>/', views.user_login_and_register, name='login-register'),
  path('home/', views.home, name='home'),
  path('profile/is-updating=<int:is_updating_user_data>', views.profile, name='profile'),
  path('vets/', views.vets, name='vets'),
  path('ai/', views.ai_page, name='ai'),
  path('', views.home, name='home'),

  path('logout/', views.user_logout, name='logout'),

  path('train_ai/', views.train_ai, name='train-ai'),
]