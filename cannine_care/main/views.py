from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.conf import settings

from .forms import CustomUserCreationForm, UserUpdateForm
from .models import CustomUser

from . import chat

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

def user_logout(request):
  logout(request)
  return redirect('home') 

@login_required(login_url='/accounts/login/') 
def home(request):
  
  base_dir = settings.BASE_DIR
  context = {}

  # Model and Intents directory
  chatbot_model_dir = str(base_dir) +"/main/chatbot-models/chatbot_2023-12-19_05-42-13.h5"
  intents_dir = str(base_dir) +"/main/dataset/intents.json"
  model_data = chat.initialize_static_chatbot_requirements(chatbot_model_dir, intents_dir)

  if request.method == 'GET':
    user_input = request.GET.get('user_input')
    if user_input:

      intents = chat.predict_class(user_input, 
        model_data['model'], 
        model_data['words'], 
        model_data['ignore_chars'],
        model_data['lemmatizer'],  
        model_data['classes'],
      )
      
      chatbot_reply = chat.get_response(intents, model_data['data'])
      return JsonResponse({'response': chatbot_reply})
  
  return render(request, 'main/home.html', context)

@login_required(login_url='/accounts/login/')
def ai_page(request):
  context = {}
  return render(request, 'main/ai.html', context)