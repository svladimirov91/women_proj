from django.contrib import admin, messages
from .models import Woman, Category


@admin.register(Woman)
class WomenAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'title',
        'time_create',
        'ispublished',
        'categ',
        'brief_info'
    )
    list_display_links = ('title',)
    ordering = ['time_create', 'title']
    list_editable = ('ispublished', )
    list_per_page = 5
    actions = ['set_published', 'set_draft']

    @admin.display(description='Краткое описание', ordering='content')
    def brief_info(self, woman: Woman):
        return f'Описание длиной {len(woman.content)} символов'

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


