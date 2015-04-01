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
                ('email', models.EmailField(max_length=75)),
                ('email_verification_code', models.TextField(max_length=64, db_index=True)),
                ('email_verified', models.BooleanField(default=False)),
                ('send_emails', models.BooleanField(default=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MavenProject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('group_id', models.TextField(max_length=512, db_index=True)),
                ('artifact_id', models.TextField(max_length=256, db_index=True)),
                ('version', models.TextField(max_length=256, db_index=True)),
                ('send_updates', models.BooleanField(default=True)),
                ('unsubscribe_code', models.TextField(max_length=64, db_index=True)),
                ('developer', models.ForeignKey(to='app.Developer', blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MavenProjectDependency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('group_id', models.TextField(max_length=512, db_index=True)),
                ('artifact_id', models.TextField(max_length=256, db_index=True)),
                ('version', models.TextField(max_length=256, blank=True)),
                ('project', models.ForeignKey(to='app.MavenProject')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MavenRepoDependency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('group_id', models.TextField(max_length=512, db_index=True)),
                ('artifact_id', models.TextField(max_length=256, db_index=True)),
                ('latest', models.TextField(max_length=256)),
                ('release', models.TextField(max_length=256)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='mavenprojectdependency',
            name='repo_version',
            field=models.ForeignKey(to='app.MavenRepoDependency', blank=True),
            preserve_default=True,
        ),
    ]
