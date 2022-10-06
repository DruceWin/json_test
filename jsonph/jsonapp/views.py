import requests
from django.shortcuts import render, get_object_or_404
from django.views import View
import json

from .models import JsonUser, JsonAlbum

# На странице кнопка которую нажимаю и я должен получить за одно нажатие одного юзера
# с ресурса https://jsonplaceholder.typicode.com/users и сохранить его в бд (поля которые нужно сохранить
# (name, username, phone, address-city)), выводить username полученного юзера на другой странице, если я
# еще раз захочу получить юзера он должен добавится в список. При нажатии на username открывается детальная
# страница о конкретном юзере где выводятся все его поля описанные выше сохранненые в бд.


class JsonPage(View):
    """Для сбора инфы с ресурса"""
    count = None
    # для счётчика, сейчас не используется
    # @classmethod
    # def counter(cls):
    #     if cls.count is None or cls.count == 9:
    #         cls.count = 0
    #     else:
    #         cls.count += 1
    #     return cls.count

    def get(self, request):
        return render(request, 'page1.html')

    def post(self, request):
        """Для загрузки пользователей и альбомов"""
        # часть загрузки юзеров
        response_api = requests.get("https://jsonplaceholder.typicode.com/users")
        data = response_api.text
        parse_json = json.loads(data)
        for i in parse_json:
            new_user = JsonUser(id_user=i['id'],
                                name=i['name'],
                                username=i['username'],
                                phone=i['phone'],
                                address_city=i['address']['city'])
            new_user.save()
        # часть загрузки альбомов
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
