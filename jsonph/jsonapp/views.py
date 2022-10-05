import requests
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

# На странице кнопка которую нажимаю и я должен получить за одно нажатие одного юзера
# с ресурса https://jsonplaceholder.typicode.com/users и сохранить его в бд (поля которые нужно сохранить
# (name, username, phone, address-city)), выводить username полученного юзера на другой странице, если я
# еще раз захочу получить юзера он должен добавится в список. При нажатии на username открывается детальная
# страница о конкретном юзере где выводятся все его поля описанные выше сохранненые в бд.
from django.views import View
import json

from .models import JsonUser, JsonAlbum


class JsonPage(View):
    count = None

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
        response_api = requests.get("https://jsonplaceholder.typicode.com/users")
        response_api_album = requests.get("https://jsonplaceholder.typicode.com/albums")
        data = response_api.text
        data_album = response_api_album.text
        parse_json = json.loads(data)
        # active_case = parse_json[self.counter()]
        # context = {'name': active_case['name'], 'username': active_case['username'], 'phone': active_case['phone'],
        # 'address_city': active_case['address']['city']}
        for i in parse_json:
            new_user = JsonUser(id_user=i['id'],
                                name=i['name'],
                                username=i['username'],
                                phone=i['phone'],
                                address_city=i['address']['city'])
            new_user.save()
        parse_json_album = json.loads(data_album)
        for di in parse_json_album:
            new_album = JsonAlbum(id_album=di['id'],
                                  id_users=di['userId'],
                                  title=di['title'])
            new_album.save()
        # return render(request, 'page1.html', context)
        return render(request, 'page1.html')


class DataBasePage(View):
    def get(self, request):
        json_users = JsonUser.objects.all()
        context = {"json_users": json_users}
        return render(request, 'page_base.html', context)


class ProfilePage(View):
    def get(self, request, id):
        json_user = get_object_or_404(JsonUser, id=id)
        json_albums = JsonAlbum.objects.get(id_users=id)
        context = {"json_user": json_user, "json_albums": json_albums}
        return render(request, 'page_profile.html', context)
