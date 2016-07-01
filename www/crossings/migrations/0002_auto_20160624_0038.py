# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-24 00:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crossings', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crossing',
            name='active',
            field=models.NullBooleanField(verbose_name='active?'),
        ),
        migrations.AlterField(
            model_name='crossing',
            name='bicycleCrossing',
            field=models.NullBooleanField(verbose_name='bicycle crossing'),
        ),
        migrations.AlterField(
            model_name='crossing',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='crossing',
            name='location1',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='location 1'),
        ),
        migrations.AlterField(
            model_name='crossing',
            name='location2',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='location 2'),
        ),
        migrations.AlterField(
            model_name='crossing',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='crossing',
            name='tcr4Survey',
            field=models.NullBooleanField(verbose_name='TCR4 survey?'),
        ),
    ]
