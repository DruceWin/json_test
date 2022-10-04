from django.contrib import admin

# Register your models here.

from .models import JsonUser

admin.site.register(JsonUser)
