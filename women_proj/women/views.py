from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseNotFound
from django.views import View
from django.views.generic import TemplateView, ListView

from .forms import AddPostForm
from .models import Woman, Category, Tag
from .utils import menu


# def index(request):
#     women_db = Woman.published.all().select_related('categ')
#     data = {
#         'title': 'Главная страница',
#         'menu': menu,
#         'posts': women_db
#     }
#     return render(request, 'women/index.html', data)

# я не понял, т.е. объекты в ListView тупо из модели передаются, получается? 
class WomenHome(ListView):
    model = Woman
    template_name = 'women/index.html'
    # context_object_name = 'posts'
    # extra_context = {
    #     'title': 'Главная страница',
    #     'menu': menu,
    #     'posts': Woman.published.all().select_related('categ')
    # }


def about(request):
    return render(request, 'women/about.html', {'title': 'О сайте', 'menu': menu})


# def add_post(request):
#     if request.method == 'POST':
#         form = AddPostForm(request.POST, request.FILES)
#         if form.is_valid():
#             # try:
#             #     Woman.objects.create(**form.cleaned_data)
#             #     return redirect('home')
#             # except Exception as exception:
#             #     form.add_error(None, exception)
#             form.save()
#             return redirect('home')
#     else:
#         form = AddPostForm()
#     data = {
#         'title': 'Добавление статьи',
#         'menu': menu,
#         'form': form
#     }
#     return render(request, 'women/add.html', context=data)


class AddPost(View):
    def get(self, request):
        form = AddPostForm()
        return render(
            request,
            'women/add.html', {
                'title': 'Добавление статьи',
                'menu': menu,
                'form': form
            }
        )

    def post(self, request):
        form = AddPostForm(request.POST, request.FILES)
        try:
            form.is_valid()
            form.save()
            return redirect('home')
        except Exception as e:
            print(type(e), str(e))
            for field_name, error in form.errors.items():
                print(f'{field_name}: {error}')
            return render(
                request,
                'women/add.html',
                {
                    'title': 'Добавление статьи',
                    'menu': menu,
                    'form': form
                }
            )


def contacts(request):
    return HttpResponse('contacts')


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
