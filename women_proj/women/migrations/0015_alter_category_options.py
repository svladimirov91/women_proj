# Generated by Django 5.0.6 on 2024-09-02 07:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('women', '0014_alter_woman_slug'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'ordering': ['name'], 'verbose_name': 'Категории', 'verbose_name_plural': 'Категории'},
        ),
    ]
