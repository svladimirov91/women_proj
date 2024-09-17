from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm


class LoginUserForm(AuthenticationForm):
    next = 'add'

    class Meta:
        model = get_user_model()
        fields = ['name', 'password']


class RegisterUserForm(forms.ModelForm):
    username = forms.CharField(label='Логин')
    password = forms.CharField(label='Пароль')
    password2 = forms.CharField(label='Повторите пароль')

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name', 'password', 'password2']
        labels = {
            'email': 'E-mail',
            'first_name': 'Имя',
            'last_name': 'Фамилия'
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return cd['password']

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError('Такой E-mail уже существует')
        return email


