# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='mavenprojectdependency',
            name='repo_version',
        ),
        migrations.AddField(
            model_name='mavenprojectdependency',
            name='repo_dependency',
            field=models.ForeignKey(blank=True, to='app.MavenRepoDependency', null=True),
            preserve_default=True,
        ),
    ]
