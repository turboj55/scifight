from django.contrib import admin
from django         import forms
from scifight import models

admin.AdminSite.site_header = 'SciFight'


class ParticipantForm(forms.ModelForm):

    class Meta:
        model = models.Participant
        exclude = []
        widgets = {
            # FIXME: Magic constant!
            'grade': forms.TextInput(attrs={'size': 5}),
        }


class ParticipantInline(admin.TabularInline):
    model = models.Participant
    form  = ParticipantForm
    extra = 0


class LeaderInline(admin.TabularInline):
    model = models.Leader
    extra = 0


@admin.register(models.Team)
class TeamAdmin(admin.ModelAdmin):
    inlines = [LeaderInline, ParticipantInline]


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
