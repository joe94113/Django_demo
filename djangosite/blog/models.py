from django.db import models


# Create your models here.

# 要在Terminal輸入
# python manage.py makemigrations blog
# python manage.py migrate
# 才可以順利創建資料表
class User(models.Model):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)


def create_user():
    # User.objects.create(firstName="Joe", lastName="Wang")  # create
    User.objects.filter(firstName="Joe", lastName="Wang").update(firstName="BigJOE")
