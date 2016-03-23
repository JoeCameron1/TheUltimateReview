# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('ultimatereview', '0004_userprofile'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paper',
            name='publish_date',
        ),
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
        migrations.RemoveField(
            model_name='review',
            name='description',
        ),
        migrations.AddField(
            model_name='paper',
            name='full_text',
            field=models.URLField(null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='query',
            name='name',
            field=models.CharField(max_length=600, null=True),
        ),
        migrations.AlterField(
            model_name='researcher',
            name='user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='review',
            name='query_string',
            field=models.CharField(default=b'', max_length=30),
        ),
        migrations.AlterField(
            model_name='review',
            name='title',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
