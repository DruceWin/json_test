from django.db import models


# сохранить его в бд (поля которые нужно сохранить
# (name, username, phone, address-city)),


class JsonUser(models.Model):
    name = models.CharField(max_length=100)
    username = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    address_city = models.CharField(max_length=100)

    def __str__(self):
        return self.name
