# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2016-03-25 00:58
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='url',
            field=models.URLField(default=datetime.datetime(2016, 3, 25, 0, 58, 22, 15383, tzinfo=utc)),
            preserve_default=False,
        ),
    ]
