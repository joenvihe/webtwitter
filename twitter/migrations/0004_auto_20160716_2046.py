# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-17 01:46
from __future__ import unicode_literals

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('twitter', '0003_profile_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='logo',
            field=models.FileField(default='settings.MEDIA_ROOT/logos/default.jpg', storage=django.core.files.storage.FileSystemStorage(location='C:\\Users\\evicente\\Documents\\PYTHON_ENV\\EV_TWITTER_V0\\webtwitter\\static\\twitter/media'), upload_to='logos'),
        ),
    ]