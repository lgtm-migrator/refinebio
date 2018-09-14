# Generated by Django 2.0.2 on 2018-09-12 18:10

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_refinery_common', '0018_organismindex_absolute_directory_path'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='experiment',
            name='protocol_description',
        ),
        migrations.AddField(
            model_name='sample',
            name='protocol_info',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={}),
        ),
    ]
