# Generated by Django 2.1.8 on 2019-07-18 18:50

from django.db import migrations


def fix_typo_in_affymetrix_samples(apps, schema_editor):
    '''Fixes affymetrix samples that have their manufacturer set to "AFFYMETRTIX" or "NEXTSEQ"
    Based off of:
    https://simpleisbetterthancomplex.com/tutorial/2017/09/26/how-to-create-django-data-migrations.html
    '''
    Sample = apps.get_model('data_refinery_common', 'Sample')

    for sample in Sample.objects.all():
        if sample.manufacturer in ("AFFYMETRTIX", "NEXTSEQ"):
            sample.manufacturer = "AFFYMETRIX"
            sample.save()


class Migration(migrations.Migration):

    dependencies = [
        ('data_refinery_common', '0022_auto_20190607_1505'),
    ]

    operations = [
        migrations.RunPython(fix_typo_in_affymetrix_samples),
    ]
