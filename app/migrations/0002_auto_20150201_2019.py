# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MavenDependency',
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
        migrations.RemoveField(
            model_name='projectdependency',
            name='latest',
        ),
        migrations.DeleteModel(
            name='LatestDependency',
        ),
        migrations.RemoveField(
            model_name='projectdependency',
            name='project',
        ),
        migrations.DeleteModel(
            name='ProjectDependency',
        ),
        migrations.AlterField(
            model_name='project',
            name='owner',
            field=models.ForeignKey(to='app.Developer', blank=True),
            preserve_default=True,
        ),
    ]
