from django.db import models
from django.urls import reverse
from django.utils.text import slugify


def translit_to_eng(s):
    d = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd',
         'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i', 'й': 'i', 'к': 'k',
         'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
         'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch',
         'ш': 'sh', 'щ': 'shch', 'ь': '', 'ы': 'y', 'ъ': '', 'э': 'a', 'ю': 'yu', 'я': 'ya'}

    res = map(lambda x: d[x] if d.get(x, False) else x, s.lower())
    return ''.join(res)


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(ispublished=Woman.Status.PUBLISHED)


class Woman(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=150, verbose_name='Заголовок')
    content = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True)

    ispublished = models.BooleanField(
        choices=tuple(map(lambda x: (bool(x[0]), x[1]), Status.choices)),
        default=Status.DRAFT,
        verbose_name='Статус'
    )

    slug = models.SlugField(
        max_length=255,
        db_index=True,
        unique=True,
        null=True,
        blank=True
    )

    categ = models.ForeignKey(
        'Category',
        on_delete=models.PROTECT,
        related_name='posts',
        verbose_name='Категория'
    )

    tags = models.ManyToManyField(
        'Tag',
        blank=True,
        # related_name='tags'
    )

    husband = models.OneToOneField(
        'Husband',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='woman'
    )

    objects = models.Manager()
    published = PublishedManager()

    photo = models.ImageField(
        upload_to='media',
        default=None,
        blank=True,
        null=True,
        verbose_name='Фото'
    )

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})

    # автоматическая генерация слагов
    def save(self, *args, **kwargs):
        print('save called')
        if not self.slug:
            title_str = str(self.title)
            self.slug = slugify(translit_to_eng(title_str))
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Известные женщины'
        verbose_name_plural = 'Известные женщины'


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(
        max_length=255,
        unique=True,
        db_index=True
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'categ_slug': self.slug})

    class Meta:
        verbose_name = 'Категории'
        verbose_name_plural = 'Категории'
        ordering = ['id']


class Tag(models.Model):
    tag = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(
        max_length=255,
        unique=True,
        db_index=True
    )

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})


class Husband(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(null=True)
    marriage_count = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return self.name

