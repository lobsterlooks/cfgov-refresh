# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2020-05-05 19:10
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import re


class Migration(migrations.Migration):

    dependencies = [
        ('regulations3k', '0031_abstracthero_and_add_jumbohero'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section',
            name='label',
            field=models.CharField(help_text='Labels always require at least 1 alphanumeric character, then any number of alphanumeric characters and hyphens, with no spaces.', max_length=255, validators=[django.core.validators.RegexValidator(re.compile('^[\\w]+[-\\w]*$', 32), 'Enter a valid “label” consisting of letters, numbers, and hyphens.', 'invalid')]),
        ),
        migrations.AlterField(
            model_name='subpart',
            name='label',
            field=models.CharField(help_text='Labels always require at least 1 alphanumeric character, then any number of alphanumeric characters and hyphens, with no spaces.', max_length=255, validators=[django.core.validators.RegexValidator(re.compile('^[\\w]+[-\\w]*$', 32), 'Enter a valid “label” consisting of letters, numbers, and hyphens.', 'invalid')]),
        ),
    ]
