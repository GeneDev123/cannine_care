from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required

from .forms import CustomUserCreationForm, UserUpdateForm
from .models import CustomUser

def user_login_and_register(request, login_or_register_param):
  if request.user.is_authenticated:
    return redirect('home')
  
  if request.method == 'POST':
    print(login_or_register_param)
    if login_or_register_param == 'login':
      form = AuthenticationForm(request, request.POST)
      if form.is_valid():
        user = form.get_user()
        login(request, user)
        return redirect('home')
    elif login_or_register_param == 'register':  
      form = CustomUserCreationForm(request.POST)
      if form.is_valid():
        user = form.save()
        login(request, user)
        return redirect('home')
  else:
    form = CustomUserCreationForm if login_or_register_param == 'register' else AuthenticationForm()

  return render(request, 'main/login-register.html', {'form': form, 'login_or_register': login_or_register_param})

@login_required(login_url='/accounts/login/') 
def home(request):
  context = {}
  
  return render(request, 'main/home.html', context)