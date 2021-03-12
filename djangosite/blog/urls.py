from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),  # 把這條路徑命名為index，呼叫views.py的index函式
    path("articles/<int:a_id>", views.view_article, name="articles"),
    path("articles/edit/<int:a_id>", views.edit_article, name="edit_articles"),
    path("author", views.author, name="author"),
    path("articles/create", views.create_article, name="create_articles"),
    path("signin", views.login, name="login"),
    path("login", views.usr_login, name="login"),
    path("logout", views.usr_logout, name="logout"),
    # path("cookies", views.cookies, name="cookies"),
    # path("get_cookies", views.get_cookies, name="get_cookies"),
    # path("get_session", views.get_session, name="get_session"),
    # path("set_session", views.set_session, name="set_session"),
    # path("snd_mail", views.snd_mail, name="send_email"),
    # path("comments", views.comments, name="comments"),
    # path("upload", views.upload_file, name="upload"),
    # path("download", views.download_file, name="download"),
]