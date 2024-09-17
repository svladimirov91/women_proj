from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseNotFound, HttpRequest, HttpResponsePermanentRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import AddPostForm
from .models import Woman, Category, Tag
from .utils import menu, DataMixin


class WomenHome(DataMixin, ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    # paginate_by = 3

    def get_queryset(self):
        return Woman.published.all().select_related('categ')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        # context['menu'] = menu
        return context

@login_required(login_url='/admin/')
def about(request):
    return render(request, 'women/about.html', {'title': 'О сайте', 'menu': menu})


class AddPost(LoginRequiredMixin, CreateView):
    form_class = AddPostForm
    template_name = 'women/add.html'
    # success_url = reverse_lazy('home') - был нужен для FormView,
    # а тут сразу перенаправление на стр. новой статьи
    extra_context = {'title': 'Добавление статьи'}
    login_url = '/admin/'

    def form_valid(self, form):
        w = form.save(commit=False)
        w.author = self.request.user
        return super().form_valid(form)


class UpdatePage(UpdateView):
    model = Woman
    fields = '__all__'
    template_name = 'women/add.html'
    extra_context = {'title': 'Редактирование статьи'}


class DeletePost(DeleteView):
    model = Woman
    template_name = 'women/confirm_delete.html'
    success_url = reverse_lazy('home')


def contacts(request):
    return HttpResponse('contacts')


class ShowPost(DetailView):
    template_name = 'women/post.html'
    slug_url_kwarg = 'post_slug'
    context_object_name = 'post'

    def get_object(self, queryset=None):
        return get_object_or_404(Woman.published, slug=self.kwargs[self.slug_url_kwarg])


class WomenCategory(DataMixin, ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_queryset(self):
        q = Woman.objects.filter(categ__slug=self.kwargs['categ_slug']).select_related('categ')
        # categ_slug берётся из адресной строки урла
        # (а вообще-то содержится в словаре kwargs объекта WomenCategory)
        category = get_object_or_404(Category, slug=self.kwargs['categ_slug'])
        q_without_fucking_around = Woman.objects.filter(categ_id=category.pk).select_related('categ')
        return q_without_fucking_around

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        categ = context['posts'][0].categ
        context['title'] = 'Категория: ' + categ.name
        context['menu'] = menu
        return context


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


class WomenTag(ListView):
    template_name = 'women/index.html'
    context_object_name = 'posts'
    allow_empty = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = Tag.objects.get(slug=self.kwargs['tag_slug'])
        context['title'] = 'Тег: ' + tag.tag
        return context

    def get_queryset(self):
        tag = get_object_or_404(Tag, slug=self.kwargs['tag_slug'])
        q = Woman.published.filter(tags=tag).select_related('categ')
        return q


def page_not_found(request, exception):
    return HttpResponseNotFound('<h1>No such page (yet)</h1>')


# OBSOLETE вьюхи:

# class AddPost(View):
#     def get(self, request):
#         form = AddPostForm()
#         return render(
#             request,
#             'women/add.html', {
#                 'title': 'Добавление статьи',
#                 'menu': menu,
#                 'form': form
#             }
#         )
#
#     def post(self, request):
#         form = AddPostForm(request.POST, request.FILES)
#         try:
#             form.is_valid()
#             form.save()
#             return redirect('home')
#         except Exception as e:
#             print(type(e), str(e))
#             for field_name, error in form.errors.items():
#                 print(f'{field_name}: {error}')
#             return render(
#                 request,
#                 'women/add.html',
#                 {
#                     'title': 'Добавление статьи',
#                     'menu': menu,
#                     'form': form
#                 }
#             )
#
# def show_by_category(request, categ_slug):
#     category = get_object_or_404(Category, slug=categ_slug)
#     posts = Woman.objects.filter(categ_id=category.pk).select_related('categ')
#     data = {
#         'title': f'Рубрика: {category.name}',
#         'menu': menu,
#         'posts': posts,
#         'categ_selected': category.pk
#     }
#     return render(request, 'women/index.html', context=data)
#
# def show_post(request, post_slug):
#     post = get_object_or_404(Woman, slug=post_slug)
#     data = {
#         'title': post.title,
#         'menu': menu,
#         'post': post,
#         'categ_selected': None
#     }
#     return render(request, 'women/post.html', context=data)

