from django.db import models
from django.contrib.auth.models import User as auth_user


# Create your models here.

# 要在Terminal輸入
# python manage.py makemigrations blog
# python manage.py migrate
# 才可以順利創建資料表
# 設定suprtuser指令
# python manage.py createsuperuser
class User(models.Model):
    firstName = models.CharField(max_length=50)
    lastName = models.CharField(max_length=50)


class Articles(models.Model):
    user = models.ForeignKey(auth_user, on_delete=models.CASCADE)  # 如果文章作者被刪除，但他有發文章會error
    content = models.CharField(max_length=50, blank=False, null=False)  # 文章不可為空
    last_updata = models.DateField(auto_now=True)


def create_user():
    User.objects.create(firstName="Joe", lastName="Wang")  # create
    # User.objects.filter(firstName="Joe", lastName="Wang")


def create_articles(content):
    user = auth_user.objects.get(username="joe")
    Articles.objects.create(user=user, content=content)
    return


def get_articles():
    user = auth_user.objects.get(username="joe")
    return Articles.objects.filter(user=user).all()

# def get_articles_owenr():
#         # article = Articles.objects.get(id=1)
#         # user = article.user
#         # 可改成以下的code
#         user = Articles.objects.get(id=1).select_related("user")
