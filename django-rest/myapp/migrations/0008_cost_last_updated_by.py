# Generated by Django 4.0.1 on 2022-02-12 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_myconfig'),
    ]

    operations = [
        migrations.AddField(
            model_name='cost',
            name='last_updated_by',
            field=models.CharField(blank=True, default='', max_length=512),
        ),
    ]
