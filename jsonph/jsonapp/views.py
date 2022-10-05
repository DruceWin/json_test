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

from .models import JsonUser


class JsonPage(View):
    def get(self, request):
        return render(request, 'page1.html')

    def post(self, request):
        response_api = requests.get("https://jsonplaceholder.typicode.com/users")
        data = response_api.text
        parse_json = json.loads(data)
        counter = 0 #не понимаю как реализовать счетчик
        active_case = parse_json[counter]
        counter += 1
        context = {'name': active_case['name'], 'username': active_case['username'], 'phone': active_case['phone'],
                   'address_city': active_case['address']['city']}
        new_user = JsonUser(name=active_case['name'],
                            username=active_case['username'],
                            phone=active_case['phone'],
                            address_city=active_case['address']['city'])
        new_user.save()
        return render(request, 'page1.html', context)


class DataBasePage(View):
    def get(self, request):
        json_users = JsonUser.objects.all()
        context = {"json_users": json_users}
        return render(request, 'page_base.html', context)


class ProfilePage(View):
    def get(self, request, id):
        json_user = get_object_or_404(JsonUser, id=id)
        context = {"json_user": json_user}
        return render(request, 'page_profile.html', context)
