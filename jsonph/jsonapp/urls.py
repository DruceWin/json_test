from django.contrib import admin
from django.urls import path

from .views import JsonPage

app_name = "jsonapp"

urlpatterns = [
    path('', JsonPage.as_view(), name='json_page'),
]