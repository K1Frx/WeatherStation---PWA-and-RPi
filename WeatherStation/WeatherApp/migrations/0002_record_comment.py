# Generated by Django 4.2.1 on 2023-05-18 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('WeatherApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='record',
            name='comment',
            field=models.CharField(blank=True, max_length=250),
        ),
    ]
