# Generated by Django 2.2.2 on 2020-12-09 07:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('grants_reports', '0004_auto_20201209_0649'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studentmonth24report',
            name='defended_proposal',
            field=models.IntegerField(choices=[(None, '--please select--'), (2, 'Yes'), (3, 'No')], null=True),
        ),
        migrations.AlterField(
            model_name='studentmonth24report',
            name='done_academic_requirements',
            field=models.IntegerField(choices=[(None, '--please select--'), (2, 'Yes'), (3, 'No')], null=True),
        ),
        migrations.AlterField(
            model_name='studentmonth24report',
            name='passed_second_courses',
            field=models.IntegerField(choices=[(None, '--please select--'), (2, 'Yes'), (3, 'No')], null=True),
        ),
        migrations.AlterField(
            model_name='studentmonth24report',
            name='progress_as_planned',
            field=models.IntegerField(choices=[(None, '--please select--'), (2, 'Yes'), (3, 'No')], null=True),
        ),
        migrations.AlterField(
            model_name='studentmonth24report',
            name='research_objectives',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='studentmonth24report',
            name='thesis_defense',
            field=models.IntegerField(choices=[(None, '--please select--'), (2, 'Yes'), (3, 'No')], null=True),
        ),
        migrations.AlterField(
            model_name='studentmonth24report',
            name='thesis_submission',
            field=models.IntegerField(choices=[(None, '--please select--'), (2, 'Yes'), (3, 'No')], null=True),
        ),
        migrations.AlterField(
            model_name='studentmonth24report',
            name='thesis_submission_external',
            field=models.IntegerField(choices=[(None, '--please select--'), (2, 'Yes'), (3, 'No')], null=True),
        ),
    ]