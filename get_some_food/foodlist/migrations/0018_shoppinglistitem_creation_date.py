# Generated by Django 3.1 on 2021-12-01 21:07

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('foodlist', '0017_product_warn_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoppinglistitem',
            name='creation_date',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
