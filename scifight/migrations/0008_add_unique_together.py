# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-07-20 07:47
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scifight', '0007_jury_make_origin_nullable'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='fight',
            unique_together=set([('room', 'fight_num')]),
        ),
        migrations.AlterUniqueTogether(
            name='fightstage',
            unique_together=set([('fight', 'action_num')]),
        ),
        migrations.AlterUniqueTogether(
            name='jurypoints',
            unique_together=set([('fight_stage', 'jury')]),
        ),
        migrations.AlterUniqueTogether(
            name='refusal',
            unique_together=set([('fight_stage', 'problem')]),
        ),
    ]