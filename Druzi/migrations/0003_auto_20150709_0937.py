# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Druzi', '0002_activity_visit_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity',
            name='limit_participants',
            field=models.IntegerField(default=0, null=True),
        ),
    ]
