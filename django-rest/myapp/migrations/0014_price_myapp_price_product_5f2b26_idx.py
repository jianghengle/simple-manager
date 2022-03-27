# Generated by Django 4.0.1 on 2022-03-25 21:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0013_price'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='price',
            index=models.Index(fields=['product_id'], name='myapp_price_product_5f2b26_idx'),
        ),
    ]
