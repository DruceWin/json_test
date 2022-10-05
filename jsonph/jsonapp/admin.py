from django.contrib import admin

# Register your models here.

from .models import JsonUser, JsonAlbum

admin.site.register(JsonUser)
admin.site.register(JsonAlbum)

