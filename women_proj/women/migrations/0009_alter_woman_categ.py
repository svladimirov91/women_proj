# Generated by Django 5.0.6 on 2024-06-21 07:28

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('women', '0008_husband_woman_husband'),
    ]

    operations = [
        migrations.AlterField(
            model_name='woman',
            name='categ',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='posts', to='women.category'),
        ),
    ]
