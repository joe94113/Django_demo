import os
import logging

from django.contrib.sessions.models import Session
from django.shortcuts import render
from django.http import HttpResponse
from django.http import request
from django.http import HttpResponseNotFound
from django.http import JsonResponse  # 可回傳json格式
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods  # 限定http傳送方式
from django.views.decorators.cache import cache_page  # 增加效能
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.core.mail import send_mail  # 發送email
from django.conf import settings  # 引入settings
from django.core.paginator import Paginator  # 分頁套件
from django.core.cache import cache

from .models import _create_articles, _get_articles, _get_articles_by_id, _edit_articles_by_id, _del_article_by_id
from .form import Django_form
from .upload import UploadFileForm
from .create_articles import create_articles_form, edit_articles_form
from .login import Login_form

# chat
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required


# chat
@login_required
def course_chat_room(request):
    return render(request, 'chat/room.html')


logger = logging.getLogger('django')

# def set_session(request):  # 設置session
#     request.session['pref'] = "C++"
#     response = HttpResponse("Session set!")
#     return response
#
#
# def get_session(request):  # 取得session
#     response = HttpResponse("Session set!" + str(request.session['pref']))
#     return response
#
#
# def get_cookies(request):  # 取得cookies
#     if "pref" in request.COOKIES:
#         print("pref:", request.COOKIES['pref'])
#         return HttpResponse("get cookies")
#     else:
#         return HttpResponse("get cookies failed")
#
#
# def cookies(request):  # 設定cookies
#     response = HttpResponse("Cookie set")
#     response.set_cookie("pref", "PYTHON")
#     return response


# Create your views here.
def index(request):  # 主畫面
    articles = _get_articles()
    content = {"articles": articles}
    return render(request, "index.html", content)


def create_article(request):  # 新增貼文
    if request.method == "POST":
        _create_articles(request)
        return redirect("index")
    else:
        form = create_articles_form
        context = {"form": form, "user": ""}
        return render(request, "create_articles.html", context)


def login(request):
    if not request.user.is_authenticated:
        return render(request, 'login.html')
    return redirect("index")


def articles(request, a_num):
    # return HttpResponse("This is articles page")
    form = Django_form()
    if request.user.is_authenticated:
        context = {"form": form, "user": request.user.username}
    else:
        context = {"form": form, "user": ""}
    return render(request, "articles.html", context)


@cache_page(60 * 15)
def author(request):
    articles = cache.get("joe")  # key
    if not articles:
        articles = _get_articles()
        cache.set("joe", articles, 30)

    paginator = Paginator(articles, 2)
    articles = paginator.get_page(request.GET["page"])

    context = {
        "name": "joe",
        "sidebar": ["Home", "Articles", "Authors"],
        "articles": articles,
    }
    return render(request, "author.html", context)
    # return redirect('articles')


def view_article(request, a_id):  # 遊覽貼文
    context = {"article": _get_articles_by_id(a_id)}
    return render(request, "show_articles.html", context)


# def create(request):
#     create_user()
#     return HttpResponse("User created")


def edit_article(request, a_id):  # 修改貼文
    if request.method == 'POST':
        _edit_articles_by_id(request, a_id)
        return redirect("index")
    else:
        form = edit_articles_form(a_id)
        context = {"form": form, "id": a_id}
        return render(request, "edit_articles.html", context)


def delete_article(request, id):
    _del_article_by_id(id)
    return redirect("index")  # 返回view index function


def upload_file(request):  # 上傳檔案
    if request.method == "POST":
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():  # 表單如果合法就儲存
            with open("/upload.txt", "wb+") as destination:  # 儲存到根目錄
                for chunk in request.FILES['file']:
                    destination.write(chunk)
                return HttpResponse("File updated")
        else:
            print("form invalid")
    else:
        form = UploadFileForm()
        return render(request, "upload.html", {"form": form})


def download_file(request):
    # file_path = os.path.join("/", "upload.txt")
    file_path = os.path.join("/upload.txt")  # 抓到要下載的檔案，要注意安全性考量不能把伺服器路徑給前端(盡量把儲存檔案位置跟程式碼分開)
    response = HttpResponse(open(file_path, "rb"), content_type="application/zip")
    response["Content-Disposition"] = "attachment; filename={}".format("download")  # 設定下載檔名
    return response


def usr_login(request):
    user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
    if user is not None:
        auth_login(request, user)
        return redirect('index')
    else:
        return redirect('usr_login')


def usr_logout(request):
    auth_logout(request)
    return redirect('index')


def snd_mail(request):
    send_mail(
        'subject here',
        'Here is the message',
        settings.EMAIL_HOST_USER,
        ['joe94113@gmail.com'],
        fail_silently=False,
    )
