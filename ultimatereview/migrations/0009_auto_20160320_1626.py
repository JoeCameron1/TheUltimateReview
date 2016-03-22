# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ultimatereview', '0008_auto_20160320_1507'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='description',
        ),
        migrations.AlterField(
            model_name='review',
            name='query_string',
            field=models.CharField(default=b'', max_length=30),
        ),
        migrations.AlterField(
            model_name='review',
            name='title',
            field=models.CharField(max_length=30),
        ),
    ]
