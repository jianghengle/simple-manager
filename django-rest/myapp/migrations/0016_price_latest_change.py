# Generated by Django 4.0.1 on 2022-04-15 04:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0015_price_flag'),
    ]

    operations = [
        migrations.AddField(
            model_name='price',
            name='latest_change',
            field=models.CharField(blank=True, default='', max_length=128),
        ),
    ]