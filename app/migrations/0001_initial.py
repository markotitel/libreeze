# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Developer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(unique=True, max_length=75)),
                ('email_verification_code', models.CharField(unique=True, max_length=64, db_index=True)),
                ('email_verification_timestamp', models.DateTimeField(blank=True)),
                ('email_verified', models.BooleanField(default=False)),
                ('send_emails', models.BooleanField(default=True)),
                ('unsubscribe_code', models.CharField(max_length=64, db_index=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('namespace', models.CharField(max_length=512, db_index=True)),
                ('name', models.CharField(max_length=256, db_index=True)),
                ('version', models.CharField(max_length=256, db_index=True)),
                ('send_updates', models.BooleanField(default=True)),
                ('unsubscribe_code', models.CharField(max_length=64, db_index=True)),
                ('developer', models.ForeignKey(to='app.Developer', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProjectDependency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('namespace', models.CharField(max_length=512, db_index=True)),
                ('name', models.CharField(max_length=256, db_index=True)),
                ('version', models.CharField(max_length=256, blank=True)),
                ('project', models.ForeignKey(to='app.Project')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='RepoDependency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('namespace', models.CharField(max_length=512, db_index=True)),
                ('name', models.CharField(max_length=256, db_index=True)),
                ('latest', models.CharField(max_length=256)),
                ('release', models.CharField(max_length=256)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='projectdependency',
            name='repo_dependency',
            field=models.ForeignKey(blank=True, to='app.RepoDependency', null=True),
            preserve_default=True,
        ),
    ]
