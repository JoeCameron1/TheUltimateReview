# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ultimatereview', '0007_auto_20160318_1920'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='title',
            field=models.CharField(unique=True, max_length=30),
        ),
    ]
