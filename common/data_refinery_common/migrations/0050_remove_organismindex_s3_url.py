# Generated by Django 2.2.7 on 2019-12-16 21:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('data_refinery_common', '0049_processorjob_abort_alter'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='organismindex',
            name='s3_url',
        ),
    ]
