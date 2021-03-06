# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-08-24 04:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_auto_20160818_0251'),
    ]

    operations = [
        migrations.CreateModel(
            name='InvitesAvailable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_type', models.CharField(choices=[('BEN', 'Beneficiary'), ('DEV', 'Developer')], default='DEV', max_length=5)),
                ('issued', models.IntegerField()),
                ('available', models.IntegerField()),
                ('last_issued', models.EmailField(blank=True, max_length=254)),
            ],
        ),
    ]
