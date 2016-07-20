from django.contrib import admin
from django         import forms
from scifight       import models

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
    model    = models.Participant
    ordering = ["short_name"]
    form     = ParticipantForm
    extra    = 0


class LeaderInline(admin.TabularInline):
    model    = models.Leader
    ordering = ["short_name"]
    extra    = 0


class RefusalInline(admin.TabularInline):
    model = models.Refusal
    extra = 0


class JuryPointsInline(admin.TabularInline):
    model = models.JuryPoints
    extra = 0


class JuryInline(admin.TabularInline):
    model = models.Fight.juries.through
    extra = 0


@admin.register(models.Team)
class TeamAdmin(admin.ModelAdmin):
    inlines = [LeaderInline, ParticipantInline]


@admin.register(models.Problem)
class ProblemAdmin(admin.ModelAdmin):
    ordering = ["problem_num"]


@admin.register(models.Fight)
class FightAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'status','start_time', 'stop_time', ]
    inlines = [JuryInline]
    exclude = ["juries"]


@admin.register(models.FightStage)
class FightStageAdmin(admin.ModelAdmin):
    inlines = [RefusalInline, JuryPointsInline]
    ordering = ["fight__fight_num", "fight__room", "action_num"]
    list_display = ["_fight_number", "_fight_room", "_action_num",
                    "_team1", "_team2", "_team3"]

    # Instead of having this method here it's possible to just
    # write "action_num" in 'list_display' parameter. But please
    # don't do that, or you would immediately get ugly arrow
    # buttons for interactive sorting. I don't like them here.
    def _action_num(self, model):
        return model.action_num

    def _fight_number(self, model):
        return model.fight.fight_num

    def _fight_room(self, model):
        return model.fight.room

    def _team1(self, model):
        return model.fight.team1

    def _team2(self, model):
        return model.fight.team2

    def _team3(self, model):
        return model.fight.team3

    # Not sure if this would help reducing the number of database
    # queries, see http://stackoverflow.com/a/28190954/1447225.
    # TODO: Check if this really helps.
    def get_queryset(self, request):
        qs = super(FightStageAdmin, self).get_queryset(request)
        return qs.select_related('fight')


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


@admin.register(models.LeaderToJury)
class LeaderToJuryAdmin(admin.ModelAdmin):
    pass
