from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Team)
admin.site.register(models.TeamOrigin)
admin.site.register(models.Participant)
admin.site.register(models.Leader)
admin.site.register(models.Jury)
admin.site.register(models.CommonOrigin)
admin.site.register(models.Fight)
admin.site.register(models.FightStage)
admin.site.register(models.Problem)
admin.site.register(models.Room)

