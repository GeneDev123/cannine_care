from django.contrib.auth.forms import UserCreationForm #UserChangeForm,
from .models import CustomUser
from django import forms

class CustomUserCreationForm(UserCreationForm):
  class Meta(UserCreationForm.Meta):
    model = CustomUser
    fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)
    
  def clean_email(self):

    email = self.cleaned_data['email'].lower()
    try:
      account = CustomUser.objects.exclude(pk=self.instance.pk).get(email=email)
    except Exception as e:
      return email
    raise forms.ValidationError('Email "%s" is already in use.' % account)

  def clean_username(self):
    username = self.cleaned_data['username']
    try:
      account = CustomUser.objects.exclude(pk=self.instance.pk).get(username=username)
    except  Exception as e:
      return username
    raise forms.ValidationError('Username "%s" is already in use.' % username)


class UserUpdateForm(forms.ModelForm):
  class Meta:
    model = CustomUser
    fields = ['username', 'first_name', 'last_name', 'bio', 'career', 'is_agree_terms_and_condition', 'profile_picture']

    def clean_username(self):
      username = self.cleaned_data['username']
      try:
        account = CustomUser.objects.exclude(pk=self.instance.pk).get(username=username)
      except  Exception as e:
        return username
      raise forms.ValidationError('Username "%s" is already in use.' % username)