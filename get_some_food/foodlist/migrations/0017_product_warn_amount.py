# Generated by Django 3.1 on 2021-12-01 19:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('foodlist', '0016_auto_20211201_2203'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='warn_amount',
            field=models.FloatField(default=1.0),
        ),
    ]
