from django.urls import path
from . import views

urlpatterns = [
    path('', views.WomenHome.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('add/', views.AddPost.as_view(), name='add'),
    path('contacts/', views.contacts, name='contacts'),
    path('post/<slug:post_slug>/', views.ShowPost.as_view(), name='post'),
    # path('post/<slug:post_slug>/', views.show_post, name='post'),
    path('category/<slug:categ_slug>/', views.WomenCategory.as_view(), name='category'),
    # path('category/<slug:categ_slug>', views.show_by_category, name='category'),
    path('tag/<slug:tag_slug>/', views.WomenTag.as_view(), name='tag'),
    # path('tag/<slug:tag_slug>', views.show_tag_postlist, name='tag')б
    path('edit/<int:pk>/', views.UpdatePage.as_view(), name='edit'),
    path('delete/<int:pk>/', views.DeletePost.as_view(), name='delete')
]
