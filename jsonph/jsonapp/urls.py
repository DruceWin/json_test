from django.urls import path

from .views import JsonPage, DataBasePage, ProfilePage, ParseUser, \
    ParseAlbums, ParsePhoto, AlbumPage, ParsePost, ParseComment, ParsePage, PostPage

app_name = "jsonapp"

urlpatterns = [
    path('', JsonPage.as_view(), name='json_page'),
    path('parse_page/', ParsePage.as_view(), name='parse_page'),
    path('parse_page/parse_user_complete/', ParseUser.as_view(), name='parse_user'),
    path('parse_page/parse_album_complete/', ParseAlbums.as_view(), name='parse_album'),
    path('parse_page/parse_photo_complete/', ParsePhoto.as_view(), name='parse_photo'),
    path('parse_page/parse_post_complete/', ParsePost.as_view(), name='parse_post'),
    path('parse_page/parse_comment_complete/', ParseComment.as_view(), name='parse_comment'),
    path('database/', DataBasePage.as_view(), name='db_page'),
    path('profile/<int:id>', ProfilePage.as_view(), name='profile_page'),
    path('album/<int:id>', AlbumPage.as_view(), name='album_page'),
    path('post/<int:id>', PostPage.as_view(), name='post_page'),
]
