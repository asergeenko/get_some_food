# Generated by Django 3.1 on 2021-12-01 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('foodlist', '0018_shoppinglistitem_creation_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoppinglistitem',
            name='purchased',
            field=models.BooleanField(default=False),
        ),
    ]
