from django.contrib import auth
from django.contrib import admin
from django         import forms
from scifight       import models
from scifight       import utils
from django.core    import exceptions

admin.AdminSite.site_header = 'SciFight'


class TournamentSpecificModelAdmin(admin.ModelAdmin):

    def get_queryset(self, request):
        self.scifight_user = request.user
        self._exclude_tournament_field()
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            tournament_of_user = None
            # To check if the (OneToOne) relation exists or not,
            # you can use the hasattr function.
            # http://stackoverflow.com/questions/3463240/check-if-onetoonefield-is-none-in-django
            if hasattr(request.user, 'scifight_user_profile'):
                scifight_user_profile = request.user.scifight_user_profile
                if scifight_user_profile.tournament:
                    tournament_of_user = scifight_user_profile.tournament
            qs = qs.filter(tournament=tournament_of_user)
        return qs

    def _exclude_tournament_field(self):
        self.exclude = ()
        if not self.scifight_user.is_superuser:
            self.exclude = ('tournament',)

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            if hasattr(request.user, 'scifight_user_profile'):
                scifight_user_profile = request.user.scifight_user_profile
                if scifight_user_profile.tournament:
                    obj.tournament = scifight_user_profile.tournament
                else:
                    raise exceptions.PermissionDenied
        obj.save()


class ParticipantForm(forms.ModelForm):

    class Meta:
        model = models.Participant
        exclude = []
        widgets = {
            # FIXME: Magic constant!
            'grade': forms.TextInput(attrs={'size': 5}),
        }


class TeamForm(forms.ModelForm):

    class Meta:
        model = models.Team
        exclude = []
        widgets = {
            # FIXME: Magic constant!
            'description': forms.Textarea(attrs={'rows':4, 'cols':40}),
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
class TeamAdmin(TournamentSpecificModelAdmin):
    fieldset = ['name']
    form = TeamForm
    inlines = [LeaderInline, ParticipantInline]
    list_display = ['name', 'origin', ]


@admin.register(models.Problem)
class ProblemAdmin(TournamentSpecificModelAdmin):
    list_display = ["problem_num", "name", '_get_short_description']
    list_display_links = ["problem_num", "name", '_get_short_description']
    ordering = ["problem_num"]

    def _get_short_description (self, model):
        return utils.shorten_text(model.description, maxchars=90)


@admin.register(models.Fight)
class FightAdmin(TournamentSpecificModelAdmin):
    list_display = ["fight_num", "room", "team1", "team2", "team3", "team4"]
    list_display_links = ["fight_num", "room"]
    list_select_related = ["room", "team1", "team2", "team3", "team4"]
    ordering = ["fight_num", "room"]
    inlines = [JuryInline]
    exclude = ["juries"]


@admin.register(models.FightStage)
class FightStageAdmin(TournamentSpecificModelAdmin):
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
class TeamOriginAdmin(TournamentSpecificModelAdmin):
    pass


@admin.register(models.Participant)
class ParticipantAdmin(TournamentSpecificModelAdmin):
    list_display = ['full_name', '_team_name', 'grade', 'is_capitan']
    ordering     = ['full_name']
    list_select_related = ['team']

    def _team_name(self, model):
        return model.team.name

    _team_name.admin_order_field = 'team__name'


@admin.register(models.Leader)
class LeaderAdmin(TournamentSpecificModelAdmin):
    list_display = ['full_name', '_team_name', 'origin']
    ordering     = ['full_name']
    list_select_related = ['team']

    def _team_name(self, model):
        return model.team.name

    _team_name.admin_order_field = 'team__name'


@admin.register(models.Jury)
class JuryAdmin(TournamentSpecificModelAdmin):
    list_display = ['full_name', '_origin_name']
    ordering     = ['full_name']
    list_select_related = ['origin']

    def _origin_name(self, model):
        return model.origin.name if model.origin else ""

    _origin_name.admin_order_field = 'origin__name'


@admin.register(models.Tournament)
class TournamentAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('short_name',)}
    list_display = ['short_name', 'slug', '_get_short_description', 'opening_date', 'closing_date']

    def _get_short_description(self, model):
        return utils.shorten_text(model.description, maxchars=90)

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


@admin.register(models.CommonOrigin)
class CommonOriginAdmin(TournamentSpecificModelAdmin):
    pass


@admin.register(models.Room)
class RoomAdmin(TournamentSpecificModelAdmin):
    pass


@admin.register(models.LeaderToJury)
class LeaderToJuryAdmin(TournamentSpecificModelAdmin):
    pass


class UserInline(admin.StackedInline):
    model = models.UserProfile


class UserAdmin(auth.admin.UserAdmin):
    inlines = [UserInline, ]


admin.site.unregister(auth.models.User)
admin.site.register(auth.models.User, UserAdmin)
