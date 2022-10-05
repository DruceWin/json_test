import requests
from django.http import JsonResponse
from django.shortcuts import render

# На странице кнопка которую нажимаю и я должен получить за одно нажатие одного юзера
# с ресурса https://jsonplaceholder.typicode.com/users и сохранить его в бд (поля которые нужно сохранить
# (name, username, phone, address-city)), выводить username полученного юзера на другой странице, если я
# еще раз захочу получить юзера он должен добавится в список. При нажатии на username открывается детальная
# страница о конкретном юзере где выводятся все его поля описанные выше сохранненые в бд.
from django.views import View
import json


class JsonPage(View):
    @staticmethod
    def get(request):
        response_API = requests.get("https://jsonplaceholder.typicode.com/users")
        data2 = response_API.text
        parse_json = json.loads(data2)

        active_case = parse_json[0]
        context = {'name': active_case['name'], 'username': active_case['username'], 'phone': active_case['phone'],
                   'address_city': active_case['address']['city']}
        return render(request, 'page1.html', context)
