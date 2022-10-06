import datetime
import random

import requests
from django.shortcuts import render, get_object_or_404
from django.views import View
import json

from .models import JsonUser, JsonAlbum, JsonPhoto, JsonPost, JsonComment


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
        return render(request, 'main_page.html')


class ParsePage(View):
    """Отображение страицы парсинга"""
    def get(self, request):
        return render(request, 'page1.html')


class ParseUser(ParsePage):
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


class ParseAlbums(ParsePage):
    def post(self, request):
        """Для загрузки альбомов"""
        response_api = requests.get("https://jsonplaceholder.typicode.com/albums")
        data = response_api.text
        parse_json = json.loads(data)

        lst = list(set([i['userId'] for i in parse_json]))
        i = 0
        json_user = get_object_or_404(JsonUser, id_user=parse_json[0]['userId'])
        for dct in parse_json:
            if dct['userId'] == lst[i]:
                new_album = JsonAlbum(id_album=dct['id'],
                                      id_users=json_user,
                                      title=dct['title'])
                new_album.save()
            else:
                i += 1
                json_user = get_object_or_404(JsonUser, id_user=dct['userId'])
                new_album = JsonAlbum(id_album=dct['id'],
                                      id_users=json_user,
                                      title=dct['title'])
                new_album.save()

        # прошлый вариант
        # for dct in parse_json:
        #     json_user = get_object_or_404(JsonUser, id_user=dct['userId'])
        #
        #     new_album = JsonAlbum(id_album=dct['id'],
        #                           id_users=json_user,
        #                           title=dct['title'])
        #     new_album.save()
        return render(request, 'page1.html')


class ParsePhoto(ParsePage):
    def post(self, request):
        """Для загрузки url фоток альбомов"""
        response_api = requests.get("https://jsonplaceholder.typicode.com/photos")
        data = response_api.text
        parse_json = json.loads(data)

        lst = list(set([i['albumId'] for i in parse_json]))
        i = 0
        json_album = get_object_or_404(JsonAlbum, id_album=parse_json[0]['albumId'])
        for dct in parse_json:
            if dct['albumId'] == lst[i]:
                new_photo = JsonPhoto(id_photo=dct['id'],
                                      id_albums=json_album,
                                      title=dct['title'],
                                      url=dct['url'],
                                      thumbnail_url=dct['thumbnailUrl'])
                new_photo.save()
            else:
                i += 1
                json_album = get_object_or_404(JsonAlbum, id_album=dct['albumId'])
                new_photo = JsonPhoto(id_photo=dct['id'],
                                      id_albums=json_album,
                                      title=dct['title'],
                                      url=dct['url'],
                                      thumbnail_url=dct['thumbnailUrl'])
                new_photo.save()

        # предыдущий вариант
        # for dct in parse_json:
        #     json_album = get_object_or_404(JsonAlbum, id_album=dct['albumId'])
        #     new_photo = JsonPhoto(id_photo=dct['id'],
        #                           id_albums=json_album,
        #                           title=dct['title'],
        #                           url=dct['url'],
        #                           thumbnail_url=dct['thumbnailUrl'])
        #     new_photo.save()
        return render(request, 'page1.html')


class ParsePost(ParsePage):
    def post(self, request):
        """Для загрузки постов"""
        response_api = requests.get("https://jsonplaceholder.typicode.com/posts")
        data = response_api.text
        parse_json = json.loads(data)
        time_for_getobject = (datetime.datetime.now()-datetime.datetime.now())
        time_for_save = (datetime.datetime.now()-datetime.datetime.now())
        for dct in parse_json:
            d = datetime.datetime.now()
            json_user = get_object_or_404(JsonUser, id_user=dct['userId'])
            time_for_getobject += (datetime.datetime.now() - d)
            new_post = JsonPost(id_post=dct['id'],
                                id_users=json_user,
                                title=dct['title'],
                                body=dct['body'])
            d2 = datetime.datetime.now()
            new_post.save()
            time_for_save += (datetime.datetime.now() - d2)
        print(time_for_getobject)
        print(time_for_save)
        return render(request, 'page1.html')


class ParseComment(ParsePage):
    def post(self, request):
        """Для загрузки комментов"""
        response_api = requests.get("https://jsonplaceholder.typicode.com/comments")
        data = response_api.text
        parse_json = json.loads(data)
        json_users = JsonUser.objects.all()
        lst_users_id = [i['id'] for i in json_users] #забрал id всех имеющихся пользователей в список
        for dct in parse_json:
            json_post = get_object_or_404(JsonPost, id_user=dct['postId'])

            lst_users_id.remove(json_post['userId']) #убрал id пользователя написавшего пост из списка
            r = random.choice(lst_users_id) #рандомно выбрал из оставшихся id

            json_user = get_object_or_404(JsonUser, id_user=r)
            new_comment = JsonComment(id_comment=dct['id'],
                                      id_posts=json_post,
                                      id_users=json_user,
                                      name=dct['name'],
                                      body=dct['body'])
            new_comment.save()
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
        json_posts = JsonAlbum.objects.filter(id_users=id)
        context = {"json_user": json_user, "json_albums": json_albums, "json_posts": json_posts}
        return render(request, 'page_profile.html', context)


class AlbumPage(View):
    def get(self, request, id):
        json_album = get_object_or_404(JsonAlbum, id=id)
        json_photos = JsonPhoto.objects.filter(id_albums=id)
        context = {"json_album": json_album, "json_photos": json_photos}
        return render(request, 'page_album.html', context)


class PostPage(View):
    def get(self, request, id):
        json_post = get_object_or_404(JsonPost, id=id)
        json_comments = JsonComment.objects.filter(id_posts=id)
        context = {"json_post": json_post, "json_comments": json_comments}
        return render(request, 'page_album.html', context)
