# Generated by Django 3.1 on 2021-11-30 19:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('foodlist', '0007_auto_20211129_1903'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoppinglistitem',
            name='due_date',
            field=models.DateField(null=True),
        ),
    ]
