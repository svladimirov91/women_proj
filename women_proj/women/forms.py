from django import forms
from .models import Category, Husband


class AddPostForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        label='Заголовок'
    )

    slug = forms.SlugField(
        max_length=255,
        label='URL'
    )

    content = forms.CharField(
        widget=forms.Textarea(),
        required=False
    )

    ispublished = forms.BooleanField(required=False)

    categ = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label='Не выбрана'
    )

    husband = forms.ModelChoiceField(
        queryset=Husband.objects.all(),
        required=False,
        empty_label='Не замужем'
    )
