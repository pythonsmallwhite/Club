# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-08-17 08:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('questions', '0004_auto_20190813_1039'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questions',
            name='title',
            field=models.CharField(max_length=255, unique=True, verbose_name='题目'),
        ),
    ]