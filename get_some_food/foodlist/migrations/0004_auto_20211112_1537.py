# Generated by Django 3.1 on 2021-11-12 12:37

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('foodlist', '0003_itemtobuy_product_purchase'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemtobuy',
            name='amount',
            field=models.FloatField(default=1.0),
        ),
        migrations.AlterField(
            model_name='purchase',
            name='amount',
            field=models.FloatField(default=1.0),
        ),
    ]
