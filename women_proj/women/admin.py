from django.contrib import admin, messages
from django.utils.safestring import mark_safe

from .models import Woman, Category


class MarriedFilter(admin.SimpleListFilter):
    title = 'Семейное положение'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [
            ('married', 'Замужем'),
            ('single', 'Не замужем')
        ]

    def queryset(self, request, queryset):
        if self.value() == 'married':
            return queryset.filter(husband__isnull=False)
        elif self.value() == 'single':
            return queryset.filter(husband__isnull=True)


@admin.register(Woman)
class WomenAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'time_create',
        'ispublished',
        'categ',
        'brief_info',
        'show_photo'
    )
    list_display_links = ('title',)
    ordering = ['time_create', 'title']
    list_editable = ('ispublished',)
    list_per_page = 15
    actions = ['set_published', 'set_draft']
    search_fields = ['title__startswith', 'categ__name']
    list_filter = [MarriedFilter, 'ispublished', 'categ__name']
    exclude = ['ispublished']
    readonly_fields = ['slug']
    filter_horizontal = ['tags']

    @admin.display(description='Краткое описание', ordering='content')
    def brief_info(self, woman: Woman):
        return f'Описание длиной {len(woman.content)} символов'

    @admin.display(description='Фотография')
    def show_photo(self, woman: Woman):
        if woman.photo:
            return mark_safe(f'<img src="{woman.photo.url}" width=50')
        return 'Нет фотографии'

    @admin.action(description='Опубликовать выбранные записи')
    def set_published(self, request, queryset):
        count = queryset.update(ispublished=Woman.Status.PUBLISHED)
        self.message_user(request, f'Изменено {count} записей')

    @admin.action(description='Снять с публикации выбранные записи')
    def set_draft(self, request, queryset):
        count = queryset.update(ispublished=Woman.Status.DRAFT)
        self.message_user(
            request,
            f'{count} записей снято с публикации',
            messages.WARNING
        )


# admin.site.register(Woman, WomenAdmin) - опционально вместо декоратора


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('name',)
    ordering = ['id']
