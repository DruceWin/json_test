from django.urls import path

from .views import JsonPage, DataBasePage, ProfilePage

app_name = "jsonapp"

urlpatterns = [
    path('', JsonPage.as_view(), name='json_page'),
    path('database/', DataBasePage.as_view(), name='db_page'),
    path('profile/<int:id>', ProfilePage.as_view(), name='profile_page'),
]