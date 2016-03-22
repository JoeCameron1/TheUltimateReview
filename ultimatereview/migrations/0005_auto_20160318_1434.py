# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ultimatereview', '0004_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='query',
            name='review',
            field=models.OneToOneField(to='ultimatereview.Review'),
        ),
    ]
