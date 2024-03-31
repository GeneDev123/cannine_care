from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from django.utils.html import format_html

admin.site.site_header = "Cannine Care Administration"

class CustomUserAdmin(UserAdmin):
  model = CustomUser

  list_display = ( 'username', 'display_profile_picture', 'is_vet', 'email', 'first_name', 'last_name', 'is_staff')

  fieldsets = (
    (None, 
      {
        'fields': ('username', 'email', 'password')
      }),
      ('Personal info', 
      {
        'fields': 
          ('profile_picture', 'first_name', 'last_name', 'bio', 'career')
      }),
      ('Vets info', 
      {
        'fields': 
          ('is_vet', 'vet_name', 'phone', 'address', 'website', 'specialization', 'hospital_affiliations')
      }),
      ('Permissions', 
      {
        'fields': 
          ('is_active', 'is_staff', 'is_superuser')
      }),
      ('Important dates', 
      {
        'fields': 
          ('last_login', 'date_joined')
      }),
      ('Agreement', 
      {
        'fields': 
          ('is_agree_terms_and_condition',)
      }),
  )

  def display_profile_picture(self, obj):
    if obj.profile_picture:
      return format_html('<img src="{}" width="50" height="50" />', obj.profile_picture.url)
    else:
      return 'No Image'

  display_profile_picture.short_description = 'Profile Picture'

admin.site.register(CustomUser, CustomUserAdmin)
