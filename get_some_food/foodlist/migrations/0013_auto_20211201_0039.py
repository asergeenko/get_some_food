# Generated by Django 3.1 on 2021-11-30 21:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('foodlist', '0012_auto_20211201_0007'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchase',
            name='amount',
        ),
        migrations.RemoveField(
            model_name='purchase',
            name='comment',
        ),
        migrations.RemoveField(
            model_name='purchase',
            name='product',
        ),
        migrations.AddField(
            model_name='purchase',
            name='item',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='foodlist.shoppinglistitem'),
            preserve_default=False,
        ),
    ]
