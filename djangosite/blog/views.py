import os

from django.shortcuts import render
from django.http import HttpResponse
from django.http import request
from django.http import HttpResponseNotFound
from django.http import JsonResponse  # 可回傳json格式
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods  # 限定http傳送方式
from django.contrib.auth import authenticate, login, logout

from .models import create_user, create_articles
from .form import Django_form
from .upload import UploadFileForm
from .login import Login_form


# Create your views here.
def index(request):
    
    return render(request, "index.html", {"form": Login_form})


@require_http_methods(["POST"])
def comments(request):
    # Save comments
    content = request.POST.get("content")  # 對應articles.html的input name
    create_articles(content)
    return HttpResponse("Comments updated!")
    # return JsonResponse({"one": "1", "two": [2, 2]})


def articles(request, a_num):
    # return HttpResponse("This is articles page")
    form = Django_form()
    if request.user.is_authenticated:
        context = {"form": form, "user": request.user.username}
    else:
        context = {"form":form, "user":""}
    return render(request, "articles.html", context)


def author(request):
    context = {
        "name": "Joe",
        "sidebar": ["Home", "Articles", "Authors"],
    }
    return render(request, "author.html", context)
    # return redirect("articles")


def create(request):
    create_user()
    return HttpResponse("User created")


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
    user = authenticate(request, username=request.POST["username"], password=request.POST["password"])
    if user is not None:
        login(request, user)
        return HttpResponse("LOGIN SUCCESSFUL :)")
    else:
        return HttpResponse("LOGIN FAILED QAQ")


def usr_logout(request):
    logout(request)
    return HttpResponse("logout successfully")