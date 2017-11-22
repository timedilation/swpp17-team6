# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-11-22 10:41
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ask', '0004_auto_20171120_0249'),
        ('location', '0002_auto_20171102_1208'),
    ]

    operations = [
        migrations.AddField(
            model_name='locationl1',
            name='questions',
            field=models.ManyToManyField(related_name='_locationl1_questions_+', to='ask.Question'),
        ),
        migrations.AddField(
            model_name='locationl2',
            name='questions',
            field=models.ManyToManyField(related_name='_locationl2_questions_+', to='ask.Question'),
        ),
        migrations.AddField(
            model_name='locationl3',
            name='questions',
            field=models.ManyToManyField(related_name='_locationl3_questions_+', to='ask.Question'),
        ),
    ]
