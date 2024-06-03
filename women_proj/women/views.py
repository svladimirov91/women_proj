from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound

from .models import Woman

menu = [
    {'title': 'О сайте', 'url_name': 'about'},
    {'title': 'Добавить статью', 'url_name': 'add'},
    {'title': 'Обратная связь', 'url_name': 'contacts'},
    {'title': 'Войти', 'url_name': 'login'}
]

categ_db = [
    {'id': 1, 'title': 'Актрисы'},
    {'id': 2, 'title': 'Певицы'},
    {'id': 3, 'title': 'Спортсменки'},
]

women_db = Woman.published.all()


def index(request):
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': women_db
    }
    return render(request, 'women/index.html', data)


def about(request):
    return render(request, 'women/about.html', {'title': 'О сайте', 'menu': menu})


def add(request):
    return HttpResponse('add')


def contacts(request):
    return HttpResponse('contacts')


def login(request):
    return HttpResponse('login')


def show_post(request, post_slug):
    post = get_object_or_404(Woman, slug=post_slug)
    data = {
        'title': post.title,
        'menu': menu,
        'post': post,
        'categ_selected': 1
    }
    return render(request, 'women/post.html', context=data)


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>No such page (yet)</h1>')
