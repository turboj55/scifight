from django.contrib import auth
from django.contrib import admin
from django         import forms
from django.utils.translation import ugettext as _tr
from scifight       import models
from scifight       import utils
from scifight       import tournament_specific

admin.AdminSite.site_header = 'SciFight'


class PersonForm(forms.ModelForm):
    identity = forms.ModelChoiceField(
        queryset    = models.PersonIdentity.objects.all(),
        empty_label = _tr("--- Create new ---"))

    class Meta:
        exclude = []


class TeamForm(forms.ModelForm):
    identity = forms.ModelChoiceField(
        queryset    = models.TeamIdentity.objects.all(),
        empty_label = _tr("--- Create new ---"))

    class Meta:
        exclude = []
        widgets = {
            # FIXME: Magic constant!
            'description': forms.Textarea(attrs={'rows':4, 'cols':40}),
        }


class ParticipantInline(tournament_specific.InlineMixin, admin.StackedInline):
    model         = models.Participant
    form          = PersonForm
    exclude       = ["tournament"]
    ordering      = ["short_name"]
    extra         = 0


class LeaderInline(tournament_specific.InlineMixin, admin.StackedInline):
    form          = PersonForm
    model         = models.Leader
    exclude       = ["tournament"]
    ordering      = ["short_name"]
    extra         = 0


class RefusalInline(tournament_specific.InlineMixin, admin.TabularInline):
    model         = models.Refusal
    exclude       = ["tournament"]
    extra         = 0


class JurorPointsInline(tournament_specific.InlineMixin, admin.TabularInline):
    model         = models.JurorPoints
    exclude       = ["tournament"]
    extra         = 0


class JurorInline(admin.TabularInline):
    model         = models.Fight.jury.through
    extra         = 0


@admin.register(models.TeamIdentity)
class TeamIdentityAdmin(admin.ModelAdmin):
    pass


@admin.register(models.PersonIdentity)
class PersonIdentityAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Team)
class TeamAdmin(tournament_specific.ModelAdmin):
    form          = TeamForm
    fieldset      = ['name']
    list_display  = ['name', 'origin', ]
    inlines       = [LeaderInline, ParticipantInline]

    class Media:
        js = ["scifight/autopopulate.js"]


@admin.register(models.Problem)
class ProblemAdmin(tournament_specific.ModelAdmin):
    ordering      = ["problem_num"]
    list_display  = ["problem_num", "title", '_get_short_description']
    list_display_links \
                  = ["problem_num", "title", '_get_short_description']

    def _get_short_description(self, model):
        return utils.shorten_text(model.description, maxchars=90)


@admin.register(models.TournamentRound)
class TournamentRoundAdmin(tournament_specific.ModelAdmin):
    ordering      = ["ordinal_num"]
    list_display  = ["ordinal_num", "opening_time", "closing_time"]


@admin.register(models.Fight)
class FightAdmin(tournament_specific.ModelAdmin):
    inlines       = [JurorInline]
    exclude       = ["jury"]
    ordering      = ["round", "room"]
    list_display  = ["round", "room",
                     "team1", "team2", "team3", "team4"]
    list_display_links \
                  = ["round", "room"]
    list_select_related \
                  = ["room", "team1", "team2", "team3", "team4"]
    foreignkey_filtered_fields \
                  = ["room", "team1", "team2", "team3", "team4"]



@admin.register(models.FightStage)
class FightStageAdmin(tournament_specific.ModelAdmin):
    inlines       = [RefusalInline, JurorPointsInline]
    ordering      = ["fight__round", "fight__room", "action_num"]
    list_display  = ["fight", "_fight_room", "_action_num",
                     "_team1", "_team2", "_team3"]
    list_select_related = ["fight"]

    tournament_alias_field     = "fight__tournament"
    foreignkey_filtered_fields = ["problem", "fight",
                                  "reporter", "opponent", "reviewer"]

    # Instead of having this method here it's possible to just
    # write "action_num" in 'list_display' parameter. But please
    # don't do that, or you would immediately get ugly arrow
    # buttons for interactive sorting. I don't like them here.
    def _action_num(self, model):
        return model.action_num

    def _fight_room(self, model):
        return model.fight.room

    def _team1(self, model):
        return model.fight.team1

    def _team2(self, model):
        return model.fight.team2

    def _team3(self, model):
        return model.fight.team3


@admin.register(models.TeamOrigin)
class TeamOriginAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Participant)
class ParticipantAdmin(tournament_specific.ModelAdmin):
    form          = PersonForm
    ordering      = ['full_name']
    list_display  = ['full_name', '_team_name', 'grade', 'is_captain']
    list_select_related = ['team']
    foreignkey_filtered_fields = ["team"]

    def _team_name(self, model):
        return model.team.name

    _team_name.admin_order_field = 'team__name'

    class Media:
        js = ["scifight/autopopulate.js"]


@admin.register(models.Leader)
class LeaderAdmin(tournament_specific.ModelAdmin):
    form          = PersonForm
    ordering      = ['full_name']
    list_display  = ['full_name', '_team_name', 'origin']
    list_select_related = ['team']
    foreignkey_filtered_fields = ["team"]

    def _team_name(self, model):
        return model.team.name

    _team_name.admin_order_field = 'team__name'

    class Media:
        js = ["scifight/autopopulate.js"]


@admin.register(models.Juror)
class JurorAdmin(tournament_specific.ModelAdmin):
    form          = PersonForm
    ordering      = ['full_name']
    list_display  = ['full_name', 'short_name', '_origin_name', 'tournament']
    list_display_links = ['full_name', 'short_name', 'tournament']
    list_select_related = ['origin']

    def _origin_name(self, model):
        return model.origin.name if model.origin else ""

    _origin_name.admin_order_field = 'origin__name'

    class Media:
        js = ["scifight/autopopulate.js"]


@admin.register(models.Tournament)
class TournamentAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('short_name',)}
    list_display = ['short_name', 'slug', '_get_short_description',
                    'opening_date', 'closing_date']

    def _get_short_description(self, model):
        return utils.shorten_text(model.description, maxchars=90)

    # TODO: Move this method into 'tournament_specific' module.
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            tournament_id = None
            if hasattr(request.user, 'scifight_user_profile'):
                if request.user.scifight_user_profile.tournament:
                    scifight_user_profile = request.user.scifight_user_profile
                    tournament_id = scifight_user_profile.tournament.id
            qs = qs.filter(id=tournament_id)
        return qs


@admin.register(models.PersonOrigin)
class CommonOriginAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Room)
class RoomAdmin(tournament_specific.ModelAdmin):
    pass

# ---


class UserInline(admin.StackedInline):
    model = models.UserProfile


class UserAdmin(auth.admin.UserAdmin):
    inlines = [UserInline, ]


admin.site.unregister(auth.models.User)
admin.site.register(auth.models.User, UserAdmin)
