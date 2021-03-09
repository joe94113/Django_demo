from django.shortcuts import render
from django.http import HttpResponse
from django.http import request
from django.http import HttpResponseNotFound
from django.http import JsonResponse  # 可回傳json格式
from django.shortcuts import render
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods  # 限定http傳送方式
from .models import create_user, create_articles


# Create your views here.
def index(request):
    return HttpResponse("HI!!!")  # 可直接塞html，也可以設定status


@require_http_methods(["POST"])
def comments(request):
    # Save comments
    content = request.POST.get("comment")  # 對應articles.html的input name
    create_articles(content)
    return HttpResponse("Comments updated!")
    # return JsonResponse({"one": "1", "two": [2, 2]})


def articles(request):
    # return HttpResponse("This is articles page")
    return render(request, "articles.html")


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
