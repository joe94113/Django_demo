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


class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=500)

    # 在前端才會顯示名稱
    def __str__(self):
        return self.name


class Articles(models.Model):
    user = models.ForeignKey(auth_user, on_delete=models.CASCADE)  # 如果文章作者被刪除，但他有發文章會error
    title = models.CharField(max_length=500, blank=False, null=False)
    content = models.CharField(max_length=500, blank=False, null=False)  # 文章不可為空
    last_updata = models.DateField(auto_now=True)
    tags = models.ManyToManyField(
        Tag,
        related_name="article_related_tags"
    )


def _create_articles(request):
    a = Articles.objects.create(user=request.user, title=request.POST['title'], content=request.POST['content'])
    query = dict(request.POST)
    for i in query['tags']:
        a.tags.add(Tag.objects.get(id=i))
    return


def _edit_articles_by_id(request, id):
    Articles.objects.filter(id=id).update(title=request.POST['title'],
                                          content=request.POST['content'])  # 利用id找到要修改文章，運用update函式修改資料
    a = Articles.objects.filter(id=id).get()
    a.tags.remove()  # Remove all of the previous tags
    query = dict(request.POST)
    for i in query['tags']:
        a.tags.add(Tag.objects.get(id=i))  # Update the new tags
    return


def _del_article_by_id(id):
    Articles.objects.filter(id=id).delete()
    return


def _get_articles():
    user = auth_user.objects.get(username="joe")
    return Articles.objects.filter(user=user).all().order_by("-last_updata")


def _get_articles_by_id(id):
    return Articles.objects.filter(id=id).first()
# def get_articles_owenr():
#         # article = Articles.objects.get(id=1)
#         # user = article.user
#         # 可改成以下的code
#         user = Articles.objects.get(id=1).select_related("user")
