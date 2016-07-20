# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db  import migrations
from scifight   import models


def create_fake_team(apps, schema_editor):
    if models.Leader.objects.count() > 0:
        fake_team = models.Team(name="--- FAKE MIGRATION TEAM, DELETE ASAP ---")
        fake_team.save()
        models.Leader.objects.update(team=fake_team)


class Migration(migrations.Migration):

    dependencies = [
        ('scifight', '0003_leader_add_team_nullable'),
    ]

    operations = [
        migrations.RunPython(
            create_fake_team,
            reverse_code=migrations.RunPython.noop),
    ]
