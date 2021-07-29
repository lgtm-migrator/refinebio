# Generated by Django 3.2.4 on 2021-07-29 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("data_refinery_common", "0067_dataset_notify_me"),
    ]

    operations = [
        migrations.AddField(
            model_name="originalfile",
            name="expected_md5",
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AddField(
            model_name="originalfile",
            name="expected_size_in_bytes",
            field=models.BigIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name="originalfile", name="md5", field=models.CharField(max_length=32, null=True),
        ),
    ]
