# Generated by Django 2.1.11 on 2019-12-20 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bluebutton', '0002_auto_20180127_2032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crosswalk',
            name='fhir_id',
            field=models.CharField(db_index=True, max_length=80, unique=True, default=None),
        ),
    ]
