# Generated by Django 2.0.7 on 2021-12-09 02:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carros', '0002_carr_preco'),
    ]

    operations = [
        migrations.AddField(
            model_name='carr',
            name='Img_url',
            field=models.TextField(default='null'),
        ),
    ]
