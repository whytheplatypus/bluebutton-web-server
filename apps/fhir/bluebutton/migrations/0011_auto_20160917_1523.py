# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-17 15:23
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bluebutton', '0010_auto_20160916_1727'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='resourcetypecontrol',
            name='resource_name',
        ),
        migrations.DeleteModel(
            name='ResourceTypeControl',
        ),
    ]
