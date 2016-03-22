# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ultimatereview', '0009_auto_20160320_1626'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='title',
            field=models.CharField(default=b'', max_length=30),
        ),
    ]
