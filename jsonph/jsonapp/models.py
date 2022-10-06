from django.db import models
from django.urls import reverse

# сохранить его в бд (поля которые нужно сохранить
# (name, username, phone, address-city)),


class JsonUser(models.Model):
    id_user = models.IntegerField()
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    address_city = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('jsonapp:profile_page', args=[self.id])


class JsonAlbum(models.Model):
    id_album = models.IntegerField()
    id_users = models.ForeignKey('JsonUser', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('jsonapp:album_page', args=[self.id])


class JsonPhoto(models.Model):
    id_photo = models.IntegerField()
    id_albums = models.ForeignKey('JsonAlbum', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    url = models.URLField(max_length=200)
    thumbnail_url = models.URLField(max_length=200)

    def __str__(self):
        return self.title
