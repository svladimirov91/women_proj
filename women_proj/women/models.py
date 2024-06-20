from django.db import models
from django.urls import reverse


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(ispublished=Woman.Status.PUBLISHED)


class Woman(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=150)
    content = models.TextField(blank=True)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    ispublished = models.BooleanField(
        choices=Status.choices,
        default=Status.DRAFT
    )
    slug = models.SlugField(
        max_length=255,
        db_index=True,
        unique=True
    )
    categ = models.ForeignKey('Category', on_delete=models.PROTECT)
    tags = models.ManyToManyField(
        'Tag',
        blank=True,
        related_name='tags'
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

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post', kwargs={'post_slug': self.slug})


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

    def __str__(self):
        return self.name

