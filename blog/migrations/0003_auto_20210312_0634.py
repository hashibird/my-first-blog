# Generated by Django 2.2.19 on 2021-03-11 21:34

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 11, 21, 34, 27, 748258, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='post',
            name='created_date',
            field=models.DateTimeField(default=datetime.datetime(2021, 3, 11, 21, 34, 27, 747285, tzinfo=utc)),
        ),
    ]