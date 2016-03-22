# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('ultimatereview', '0006_auto_20160318_1910'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='researcher',
            name='email',
        ),
        migrations.RemoveField(
            model_name='researcher',
            name='password',
        ),
        migrations.RemoveField(
            model_name='researcher',
            name='user_name',
        ),
        migrations.AlterField(
            model_name='researcher',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
    ]
