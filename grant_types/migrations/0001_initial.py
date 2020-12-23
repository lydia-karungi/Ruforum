# Generated by Django 2.2.2 on 2020-12-03 06:07

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Granttype',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('instructions', models.FileField(upload_to='')),
                ('template', models.FileField(upload_to='')),
                ('require_other_universities', models.BooleanField()),
                ('require_collaborator_cvs', models.BooleanField()),
                ('require_supporting_letters', models.BooleanField()),
                ('require_project_budget', models.BooleanField()),
                ('project_budget_template', models.FileField(upload_to='')),
                ('review_form_template', models.FileField(upload_to='')),
            ],
        ),
    ]