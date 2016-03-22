# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Paper',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=30)),
                ('authors', models.CharField(max_length=30)),
                ('abstract', models.CharField(max_length=300)),
                ('publish_date', models.DateField()),
                ('paper_url', models.URLField()),
                ('abstract_relevance', models.CharField(max_length=30)),
                ('document_relevance', models.CharField(max_length=30)),
                ('notes', models.CharField(max_length=30)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Query',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Researcher',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user_name', models.CharField(max_length=30)),
                ('password', models.CharField(max_length=30)),
                ('email', models.CharField(max_length=30)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Review',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=30)),
                ('description', models.CharField(max_length=300)),
                ('date_started', models.DateField()),
                ('query_string', models.CharField(max_length=30)),
                ('pool_size', models.IntegerField(default=0)),
                ('abstracts_judged', models.IntegerField(default=0)),
                ('document_judged', models.IntegerField(default=0)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='paper',
            name='review',
            field=models.ForeignKey(to='ultimatereview.Review'),
            preserve_default=True,
        ),
    ]
