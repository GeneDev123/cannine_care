from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
  
  bio = models.TextField(blank=True, null=True)
  first_name = models.CharField(max_length=100, blank=True, null=True,)
  last_name = models.CharField(max_length=100, blank=True, null=True,)
  is_agree_terms_and_condition = models.BooleanField(default=False)
  career = models.CharField(max_length=255, blank=True, null=True,)
  profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)

  # ===== For Profile Page =====
  is_vet = models.BooleanField(default=False)
  vet_name = models.CharField(max_length=100, blank=True, null=True,)
  phone = models.CharField(max_length=20, null=True, blank=True)
  address = models.TextField(null=True, blank=True)
  website = models.URLField(null=True, blank=True)
  specialization = models.TextField(null=True, blank=True)
  hospital_affiliations = models.TextField(null=True, blank=True)

  def __str__(self):
    return f"{self.first_name} {self.last_name}"