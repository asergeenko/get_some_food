# Generated by Django 3.1 on 2021-11-30 20:22

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('foodlist', '0010_auto_20211130_2319'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoppinglist',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
