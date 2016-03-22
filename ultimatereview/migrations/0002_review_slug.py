# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
        ('ultimatereview', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='slug',
            field=models.SlugField(default=datetime.date(2016, 3, 17)),
            preserve_default=False,
        ),
    ]
