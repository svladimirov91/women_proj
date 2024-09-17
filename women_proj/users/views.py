from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import LoginUserForm, RegisterUserForm


# def user_login(request):
#     if request.method == 'POST':
#         form = LoginUserForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(
#                 request,
#                 username=cd['username'],
#                 password=cd['password']
#             )
#             if user and user.is_active:
#                 login(request, user)
#                 return HttpResponseRedirect(reverse('home'))
#     else:
#         form = LoginUserForm()
#     return render(request, 'users/user_login.html', {'form': form})
class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'users/user_login.html'
    extra_context = {'title': 'Авторизация'}


def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('user_login'))


def register(request):
    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return render(request, 'users/reg_successful.html')
    else:
        form = RegisterUserForm()
    return render(request, 'users/register.html', {'form': form})
