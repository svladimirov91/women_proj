# Generated by Django 5.0.6 on 2024-09-02 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('women', '0016_alter_category_options'),
    ]

    operations = [
        migrations.AlterField(
            model_name='woman',
            name='slug',
            field=models.SlugField(blank=True, max_length=255, null=True, unique=True),
        ),
    ]
