# Generated by Django 3.1 on 2021-11-12 12:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('foodlist', '0002_auto_20211112_1512'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('shelf_life', models.DurationField(blank=True, null=True)),
                ('category',
                 models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='foodlist.category')),
                ('unit', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foodlist.unit')),
            ],
        ),
        migrations.CreateModel(
            name='Purchase',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('buy_date', models.DateField(auto_now_add=True)),
                ('amount', models.SmallIntegerField(default=1)),
                ('comment', models.TextField(blank=True)),
                ('expiry_date', models.DateField()),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foodlist.product')),
            ],
        ),
        migrations.CreateModel(
            name='ItemToBuy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.SmallIntegerField(default=1)),
                ('comment', models.TextField(blank=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='foodlist.product')),
            ],
        ),
    ]
