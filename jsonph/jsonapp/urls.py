from django.urls import path

from .views import JsonPage, DataBasePage, ProfilePage, ParseUser, ParseAlbums, ParsePhoto, AlbumPage

app_name = "jsonapp"

urlpatterns = [
    path('', JsonPage.as_view(), name='json_page'),
    path('parse_user_complete/', ParseUser.as_view(), name='parse_user'),
    path('parse_album_complete/', ParseAlbums.as_view(), name='parse_album'),
    path('parse_photo_complete/', ParsePhoto.as_view(), name='parse_photo'),
    path('database/', DataBasePage.as_view(), name='db_page'),
    path('profile/<int:id>', ProfilePage.as_view(), name='profile_page'),
    path('album/<int:id>', AlbumPage.as_view(), name='album_page'),
]
