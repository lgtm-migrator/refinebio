# Generated by Django 3.1.7 on 2021-03-24 19:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data_refinery_common', '0064_auto_20210225_1622'),
    ]

    operations = [
        migrations.AlterField(
            model_name='computationalresultannotation',
            name='data',
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='data',
            field=models.JSONField(default=dict, help_text="This is a dictionary where the keys are experiment accession codes and the values are lists with sample accession codes. Eg: `{'E-ABC-1': ['SAMP1', 'SAMP2']}`"),
        ),
        migrations.AlterField(
            model_name='dataset',
            name='success',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='datasetannotation',
            name='data',
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='downloaderjob',
            name='success',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='experiment',
            name='protocol_description',
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='experimentannotation',
            name='data',
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='processor',
            name='environment',
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='processorjob',
            name='success',
            field=models.BooleanField(null=True),
        ),
        migrations.AlterField(
            model_name='sample',
            name='protocol_info',
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='sampleannotation',
            name='data',
            field=models.JSONField(default=dict),
        ),
        migrations.AlterField(
            model_name='surveyjob',
            name='success',
            field=models.BooleanField(null=True),
        ),
    ]
