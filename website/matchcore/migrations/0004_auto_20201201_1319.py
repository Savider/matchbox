# Generated by Django 3.1.3 on 2020-12-01 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matchcore', '0003_auto_20201128_2012'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projecttag',
            name='img',
        ),
        migrations.AlterField(
            model_name='usertag',
            name='img',
            field=models.ImageField(upload_to='tags'),
        ),
    ]
