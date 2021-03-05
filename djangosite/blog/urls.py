from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),  # 把這條路徑命名為index，呼叫views.py的index函式
    path("articles", views.articles, name="articles"),
    path("author", views.author, name="author"),
    path("comments", views.comments, name="comments"),
    path("create", views.create, name="create"),
]