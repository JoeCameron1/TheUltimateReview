# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ultimatereview', '0012_auto_20160320_1715'),
    ]

    operations = [
        migrations.AlterField(
            model_name='query',
            name='name',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
