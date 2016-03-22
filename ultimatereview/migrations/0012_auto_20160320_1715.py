# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ultimatereview', '0011_auto_20160320_1709'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='title',
            field=models.CharField(max_length=30, null=True),
        ),
    ]
