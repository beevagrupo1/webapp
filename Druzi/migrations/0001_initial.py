# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import geoposition.fields


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=150)),
                ('description', models.TextField(max_length=500)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('modification_date', models.DateTimeField(auto_now_add=True, null=True)),
                ('activity_date', models.DateTimeField()),
                ('position', geoposition.fields.GeopositionField(max_length=42)),
                ('place_name', models.CharField(max_length=150)),
                ('price', models.FloatField(default=0.0)),
                ('limit_participants', models.IntegerField(null=True)),
                ('parent', models.ForeignKey(to='Druzi.Activity', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Enrollment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('activity', models.ForeignKey(to='Druzi.Activity')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('name', models.CharField(max_length=50, serialize=False, primary_key=True)),
                ('count', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='TagAppear',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('position', models.IntegerField()),
                ('activity', models.ForeignKey(to='Druzi.Activity')),
                ('tag', models.ForeignKey(to='Druzi.Tag')),
            ],
        ),
        migrations.AddField(
            model_name='tag',
            name='activity',
            field=models.ManyToManyField(related_name='activities', through='Druzi.TagAppear', to='Druzi.Activity'),
        ),
        migrations.AddField(
            model_name='activity',
            name='participants',
            field=models.ManyToManyField(default=0, related_name='participants', through='Druzi.Enrollment', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='activity',
            name='tags',
            field=models.ManyToManyField(related_name='tags', through='Druzi.TagAppear', to='Druzi.Tag'),
        ),
        migrations.AddField(
            model_name='activity',
            name='user_own',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(
            name='enrollment',
            unique_together=set([('activity', 'user')]),
        ),
    ]
