# Generated by Django 3.2.7 on 2021-12-08 21:18

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data_refinery_common", "0069_rename_compendia_version_computedfile_compendium_version"),
    ]

    operations = [
        migrations.AddField(
            model_name="sample",
            name="is_unable_to_be_processed",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="sample",
            name="last_downloader_job",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="data_refinery_common.downloaderjob",
            ),
        ),
        migrations.AddField(
            model_name="sample",
            name="last_processor_job",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="data_refinery_common.processorjob",
            ),
        ),
        migrations.AddField(
            model_name="sample",
            name="most_recent_quant_file",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="data_refinery_common.computedfile",
            ),
        ),
        migrations.AddField(
            model_name="sample",
            name="most_recent_smashable_file",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="data_refinery_common.computedfile",
            ),
        ),
    ]
