from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

class CustomUserAdmin(UserAdmin):
  model = CustomUser

  list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')

  fieldsets = (
    (None, 
      {
        'fields': ('username', 'email', 'password')
      }),
      ('Personal info', 
      {
        'fields': 
          ('first_name', 'last_name', 'bio', 'career')
      }),
      ('Permissions', 
      {
        'fields': 
          ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
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

admin.site.register(CustomUser, CustomUserAdmin)
