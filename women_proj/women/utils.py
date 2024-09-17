menu = [
    {'title': 'О сайте', 'url_name': 'about'},
    {'title': 'Добавить статью', 'url_name': 'add'},
    {'title': 'Обратная связь', 'url_name': 'contacts'},
    {'title': 'Войти', 'url_name': 'user_login'}
]

post_buttons = [
    {'name': 'Редактировать статью', 'url': 'edit'},
    {'name': 'Удалить статью', 'url': 'delete'}
]

options = [
    ('Опция 1', 'URL 1'),
    ('Опция 2', 'URL 2'),
    ('Опция 3', 'URL 3'),
    ('Опция 4', 'URL 4'),
    ('Опция 5', 'URL 5'),
    ('Опция 6', 'URL 6'),
    ('Опция 7', 'URL 7'),
]
context_processor_options = [dict(name=x, url=y) for x, y in options]


class DataMixin:
    paginate_by = 3

    def get_mixin_context(self, context, **kwargs):
        context.update(kwargs)
        return context
