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
class FightStageAdmin(admin.ModelAdmin):
    pass


@admin.register(models.TeamOrigin)
class TeamOriginAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Participant)
class TeamOriginAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Leader)
class LeaderAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Jury)
class JuryAdmin(admin.ModelAdmin):
    pass


@admin.register(models.CommonOrigin)
class CommonOriginAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):
    pass


@admin.register(models.JuryPoints)
class JuryPointsAdmin(admin.ModelAdmin):
    pass
