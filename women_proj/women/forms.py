from django import forms
from django.core.exceptions import ValidationError

from .models import Category, Husband, Woman

class AddPostForm(forms.ModelForm):
    categ = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label='Категория не выбрана',
        label='Категория'
    )

    husband = forms.ModelChoiceField(
        queryset=Husband.objects.all(),
        empty_label='Не замужем',
        required=False,
        label='Муж'
    )

    class Meta:
        model = Woman
        fields = [
            'title',
            'slug',
            'content',
            'ispublished',
            'categ',
            'husband',
            'tags',
            'photo'
        ]

    #  валидатор для заголовка
    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) > 50:
            raise ValidationError('Длина не должна превышать 50 символов')
        return title
