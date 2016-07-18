from django.contrib import admin
from scifight import models

admin.AdminSite.site_header = 'SciFight'


@admin.register(models.Team)
class TeamAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Problem)
class ProblemAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Fight)
class FightAdmin(admin.ModelAdmin):
    pass


@admin.register(models.FightStage)
class AdminFightStage(admin.ModelAdmin):
    pass


@admin.register(models.TeamOrigin)
class AdminTeamOrigin(admin.ModelAdmin):
    pass


@admin.register(models.Participant)
class AdminTeamOrigin(admin.ModelAdmin):
    pass


@admin.register(models.Leader)
class AdminLeader(admin.ModelAdmin):
    pass


@admin.register(models.Jury)
class AdminJury(admin.ModelAdmin):
    pass


@admin.register(models.CommonOrigin)
class AdminCommonOrigin(admin.ModelAdmin):
    pass


@admin.register(models.Room)
class AdminRoom(admin.ModelAdmin):
    pass


@admin.register(models.JuryPoints)
class AdminJuryPoints(admin.ModelAdmin):
    pass
