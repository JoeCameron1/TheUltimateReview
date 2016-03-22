# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ultimatereview', '0002_review_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='query',
            name='review',
            field=models.ForeignKey(default='', to='ultimatereview.Review'),
            preserve_default=False,
        ),
    ]
