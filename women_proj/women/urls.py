from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('add/', views.add_post, name='add'),
    path('contacts/', views.contacts, name='contacts'),
    path('login/', views.login, name='login'),
    path('post/<slug:post_slug>/', views.show_post, name='post'),
    path('category/<slug:categ_slug>', views.show_by_category, name='category'),
    path('tag/<slug:tag_slug>', views.show_tag_postlist, name='tag')
]

