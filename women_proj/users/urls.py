from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginUser.as_view(), name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('register/', views.register, name='register')
]
