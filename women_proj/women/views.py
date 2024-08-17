from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseNotFound

from .forms import AddPostForm
from .models import Woman, Category, Tag

menu = [
    {'title': 'О сайте', 'url_name': 'about'},
    {'title': 'Добавить статью', 'url_name': 'add'},
    {'title': 'Обратная связь', 'url_name': 'contacts'},
    {'title': 'Войти', 'url_name': 'login'}
]


def index(request):
    women_db = Woman.published.all().select_related('categ')
    data = {
        'title': 'Главная страница',
        'menu': menu,
        'posts': women_db
    }
    return render(request, 'women/index.html', data)


def about(request):
    return render(request, 'women/about.html', {'title': 'О сайте', 'menu': menu})


def add_post(request):
    if request.method == 'POST':
        print('POST REQUEST')
        form = AddPostForm(request.POST)
        # if form.is_valid():
        #     try:
        #         Woman.objects.create(**form.cleaned_data)
        #         return redirect('home')
        #     except Exception:
        #         form.add_error(None, 'Ошибка добавления поста')
    else:
        print('GET REQUEST')
        form = AddPostForm()
    data = {
        'title': 'Добавление статьи',
        'menu': menu,
        'form': form
    }
    return render(request, 'women/add.html', context=data)


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
        'categ_selected': None
    }
    return render(request, 'women/post.html', context=data)


def show_by_category(request, categ_slug):
    category = get_object_or_404(Category, slug=categ_slug)
    posts = Woman.objects.filter(categ_id=category.pk).select_related('categ')
    data = {
        'title': f'Рубрика: {category.name}',
        'menu': menu,
        'posts': posts,
        'categ_selected': category.pk
    }
    return render(request, 'women/index.html', context=data)


def show_tag_postlist(request, tag_slug):
    tag = get_object_or_404(Tag, slug=tag_slug)
    posts = tag.woman_set.filter(ispublished=Woman.Status.PUBLISHED).select_related('categ')
    data = {
        'title': f'Тег: {tag.tag}',
        'menu': menu,
        'posts': posts,
        'categ_selected': None
    }

    return render(request, 'women/index.html', context=data)


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>No such page (yet)</h1>')
