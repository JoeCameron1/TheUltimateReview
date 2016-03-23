# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ultimatereview', '0013_auto_20160321_2008'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='paper',
            name='publish_date',
        ),
        migrations.AlterField(
            model_name='query',
            name='name',
            field=models.CharField(max_length=600, null=True),
        ),
    ]
