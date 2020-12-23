# Generated by Django 2.2.2 on 2020-12-10 14:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hrm', '0014_auto_20201210_1203'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='appraisal',
            name='competency',
        ),
        migrations.RemoveField(
            model_name='appraisal',
            name='leadership_competency',
        ),
        migrations.RemoveField(
            model_name='appraisal',
            name='staff',
        ),
        migrations.DeleteModel(
            name='PerformanceTarget',
        ),
        migrations.AlterField(
            model_name='leaveapplication',
            name='supervisor_comment',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='Appraisal',
        ),
    ]