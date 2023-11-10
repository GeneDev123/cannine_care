from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
  
  bio = models.TextField(blank=True, null=True)
  first_name = models.CharField(max_length=100, blank=True, null=True,)
  last_name = models.CharField(max_length=100, blank=True, null=True,)
  is_agree_terms_and_condition = models.BooleanField(default=False)
  career = models.CharField(max_length=255, blank=True, null=True,)

  def __str__(self):
    return f"{self.first_name} {self.last_name}"