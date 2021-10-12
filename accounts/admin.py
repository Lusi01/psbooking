from django.contrib import admin
from . import models


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'phone', 'country', 'city', 'role']
    fields = ['user', 'avatar', 'phone', 'country', 'city', 'role']

