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
        data = {
            "name": "Leanne Graham",
            "username": "Bret",
            "address": {
                "street": "Kulas Light",
                "suite": "Apt. 556",
                "city": "Gwenborough",
                "zipcode": "92998-3874",
                "geo": {
                    "lat": "-37.3159",
                    "lng": "81.1496"
                }
            },
            "phone": "1-770-736-8031 x56442",
        }
        response_API = requests.get("https://jsonplaceholder.typicode.com/users")
        data2 = response_API.text
        parse_json = json.loads(data2)
        print(parse_json)
        active_case = parse_json[0]
        return JsonResponse(active_case)
