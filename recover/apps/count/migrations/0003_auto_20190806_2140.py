# -*- coding: utf-8 -*-
# Generated by Django 1.11.20 on 2019-08-06 13:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('count', '0002_auto_20190806_2102'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='category_name',
            field=models.CharField(default=10, max_length=12),
        ),
    ]