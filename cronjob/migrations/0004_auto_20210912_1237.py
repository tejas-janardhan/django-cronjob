# Generated by Django 3.2.5 on 2021-09-12 16:37

import cronjob.db_fields
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('cronjob', '0003_alter_jobhistory_date_ended'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='jobgroup',
            name='date_created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='job',
            name='_args',
            field=models.CharField(blank=True, default='', help_text='Enter elements of the array seperated by a comma, e.g. arg1,arg2..argN', max_length=100),
        ),
        migrations.AlterField(
            model_name='job',
            name='job_path',
            field=cronjob.db_fields.PythonFunctionField(help_text='Module path followed by the function name. eg. cronjob.jobs.test_function.', max_length=100),
        ),
    ]