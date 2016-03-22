# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ultimatereview', '0005_auto_20160318_1434'),
    ]

    operations = [
        migrations.AlterField(
            model_name='query',
            name='review',
            field=models.ForeignKey(to='ultimatereview.Review'),
        ),
    ]
