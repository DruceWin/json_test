import requests
from django.shortcuts import render, get_object_or_404
from django.views import View
import json

from .models import JsonUser, JsonAlbum, JsonPhoto


# На странице кнопка которую нажимаю и я должен получить за одно нажатие одного юзера
# с ресурса https://jsonplaceholder.typicode.com/users и сохранить его в бд (поля которые нужно сохранить
# (name, username, phone, address-city)), выводить username полученного юзера на другой странице, если я
# еще раз захочу получить юзера он должен добавится в список. При нажатии на username открывается детальная
# страница о конкретном юзере где выводятся все его поля описанные выше сохранненые в бд.


class JsonPage(View):
    """Отображение главной страицы"""
    count = None
    # для счётчика, сейчас не используется
    @classmethod
    def counter(cls):
        if cls.count is None or cls.count == 9:
            cls.count = 0
        else:
            cls.count += 1
        return cls.count

    def get(self, request):
        return render(request, 'page1.html')


class ParseUser(View):
    def post(self, request):
        """Для загрузки пользователей и альбомов"""
        # часть загрузки юзеров
        response_api = requests.get("https://jsonplaceholder.typicode.com/users")
        data = response_api.text
        parse_json = json.loads(data)
        for dct in parse_json:
            new_user = JsonUser(id_user=dct['id'],
                                name=dct['name'],
                                username=dct['username'],
                                phone=dct['phone'],
                                address_city=dct['address']['city'])
            new_user.save()
        return render(request, 'page1.html')


class ParseAlbums(View):
    def post(self, request):
        """Для загрузки альбомов"""
        response_api_album = requests.get("https://jsonplaceholder.typicode.com/albums")
        data_album = response_api_album.text
        parse_json_album = json.loads(data_album)
        for dct in parse_json_album:
            json_user = get_object_or_404(JsonUser, id_user=dct['userId'])
            new_album = JsonAlbum(id_album=dct['id'],
                                  id_users=json_user,
                                  title=dct['title'])
            new_album.save()
        return render(request, 'page1.html')


class ParsePhoto(View):
    def post(self, request):
        """Для загрузки url фоток альбомов"""
        response_api_photo = requests.get("https://jsonplaceholder.typicode.com/photos")
        data_photo = response_api_photo.text
        parse_json_photo = json.loads(data_photo)
        for dct in parse_json_photo:
            json_album = get_object_or_404(JsonAlbum, id_album=dct['albumId'])
            new_photo = JsonPhoto(id_photo=dct['id'],
                                  id_albums=json_album,
                                  title=dct['title'],
                                  url=dct['url'],
                                  thumbnail_url=dct['thumbnailUrl'])
            new_photo.save()
        return render(request, 'page1.html')


class DataBasePage(View):
    """Отображение всех пользователей"""
    def get(self, request):
        json_users = JsonUser.objects.all()
        context = {"json_users": json_users}
        return render(request, 'page_base.html', context)


class ProfilePage(View):
    """Отображение профиля со всеми альбомами пользователя"""
    def get(self, request, id):
        json_user = get_object_or_404(JsonUser, id=id)
        json_albums = JsonAlbum.objects.filter(id_users=id)
        context = {"json_user": json_user, "json_albums": json_albums}
        return render(request, 'page_profile.html', context)


class AlbumPage(View):
    def get(self, request, id):
        json_album = get_object_or_404(JsonAlbum, id=id)
        json_photos = JsonPhoto.objects.filter(id_albums=id)
        context = {"json_album": json_album, "json_photos": json_photos}
        return render(request, 'page_album.html', context)
