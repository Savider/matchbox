# Generated by Django 3.1.3 on 2020-12-01 14:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matchcore', '0008_user_img'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='discord',
            field=models.CharField(default='None', max_length=30),
        ),
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(default='0', max_length=10),
        ),
    ]
