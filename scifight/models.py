from django.db   import models
from django.core import exceptions
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.translation   import ugettext as _tr

SLUG_LENGTH = 20
""" Maximum length of slug fields. This value must be large enough to hold
    a URL path component of reasonable length. No one is going to remember
    and read overly long addresses."""

NAME_LENGTH = 140
""" Maximum length of name fields in various models. This value should be
    long enough to hold any reasonable personal name, university name, district
    name, or other things like these. """

TEXT_LENGTH = 1024
""" Maximum length of descriptions fields in models below. This value should be
    long enough to hold an average paragraph of descriptive text. Maybe,
    a thousand or two of characters. """

GRADE_LENGTH = 20
""" Maximum length of the `grade` field. This value should be long enough to
    hold a number plus possible brief one-word explanation. """


class TeamIdentity(models.Model):

    def __str__(self):
        # For people to be able to guess where *exactly* they may have seen
        # this team before, show it's latest known name and tournament it
        # participated in.
        latest_team = self.teams.order_by("-tournament__closing_date").first()
        if latest_team:
            return _tr("TID#{0}: «{1}» on {2}").format(self.pk,
                                             latest_team.name,
                                             latest_team.tournament.short_name)
        else:
            return _tr("TID#{0}").format(self.pk)


class PersonIdentity(models.Model):

    def __str__(self):

        # Shorthand function. Will return 'None' if nothing is found.
        def get_most_recent(objs: models.manager.Manager):
            return objs.order_by("-tournament__closing_date").first()

        latest_juror       = get_most_recent(self.jury)
        latest_leader      = get_most_recent(self.leaders)
        latest_participant = get_most_recent(self.participants)

        avatars = {latest_juror, latest_leader, latest_participant}
        avatars.remove(None)

        if not avatars:
            return _tr("HID#{0}").format(self.pk)

        latest_avatar = max(avatars, key=lambda a: a.tournament.closing_date)
        return _tr("HID#{0}: {1} on {2}").format(self.pk,
                                        latest_avatar.short_name,
                                        latest_avatar.tournament.short_name)


class TeamOrigin(models.Model):
    place_name    = models.CharField(max_length=NAME_LENGTH)

    def __str__(self):
        return self.place_name

    class Meta:
        verbose_name        = _tr("Team origin")
        verbose_name_plural = _tr("Team origins")


class PersonOrigin(models.Model):
    place_name    = models.CharField(max_length=NAME_LENGTH)

    def __str__(self):
        return self.place_name


class Tournament(models.Model):
    full_name     = models.CharField(max_length=NAME_LENGTH)
    short_name    = models.CharField(max_length=NAME_LENGTH)
    slug          = models.SlugField(max_length=SLUG_LENGTH, unique=True)
    description   = models.TextField(blank=True, null=True)
    opening_date  = models.DateField(default=timezone.now)
    closing_date  = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.short_name


class Team(models.Model):
    tournament    = models.ForeignKey(Tournament)
    identity      = models.ForeignKey(TeamIdentity, related_name="teams")
    name          = models.CharField(max_length=NAME_LENGTH)
    slug          = models.SlugField(max_length=SLUG_LENGTH,
                                     null=True, blank=True)
    description   = models.TextField(max_length=TEXT_LENGTH, blank=True)
    origin        = models.ForeignKey(TeamOrigin, null=True, blank=True)

    def clean(self):
        super().clean()

        # Force Django to always store SQL NULL for slug instead of an empty
        # string, thus making 'unique_together' work again.
        # NOTE: in SQL NULLs are treated as unique values.
        if self.slug == "":
            self.slug = None

    def __str__(self):
        return self.name

    class Meta:
        unique_together = ('tournament', 'slug')


class Participant(models.Model):
    tournament    = models.ForeignKey(Tournament)
    identity      = models.ForeignKey(PersonIdentity,
                                      related_name="participants")
    full_name     = models.CharField(max_length=NAME_LENGTH)
    short_name    = models.CharField(max_length=NAME_LENGTH)
    origin        = models.ForeignKey(PersonOrigin, null=True, blank=True)
    grade         = models.CharField(max_length=GRADE_LENGTH, blank=True)
    team          = models.ForeignKey(Team)
    is_captain    = models.BooleanField()

    def fill_tournament(self):
        self.tournament = self.team.tournament

    def __str__(self):
        return self.short_name


class Leader(models.Model):
    tournament    = models.ForeignKey(Tournament)
    identity      = models.ForeignKey(PersonIdentity, related_name="leaders")
    full_name     = models.CharField(max_length=NAME_LENGTH)
    short_name    = models.CharField(max_length=NAME_LENGTH)
    origin        = models.ForeignKey(PersonOrigin, null=True, blank=True)
    team          = models.ForeignKey(Team)

    def fill_tournament(self):
        self.tournament = self.team.tournament

    def __str__(self):
        return self.short_name


class Juror(models.Model):
    tournament    = models.ForeignKey(Tournament)
    identity      = models.ForeignKey(PersonIdentity, related_name="jury")
    full_name     = models.CharField(max_length=NAME_LENGTH)
    short_name    = models.CharField(max_length=NAME_LENGTH)
    origin        = models.ForeignKey(PersonOrigin, null=True, blank=True)

    def __str__(self):
        return self.short_name


class Room(models.Model):
    tournament    = models.ForeignKey(Tournament)
    designation   = models.CharField(max_length=NAME_LENGTH)

    def __str__(self):
        return self.designation


class Problem(models.Model):
    tournament    = models.ForeignKey(Tournament)
    problem_num   = models.IntegerField(primary_key=True)
    title         = models.CharField(max_length=NAME_LENGTH)
    description   = models.TextField(max_length=TEXT_LENGTH, blank=True)

    def __str__(self):
        return _tr("#{0}. {1}").format(self.problem_num, self.title)


class TournamentRound(models.Model):
    tournament    = models.ForeignKey(Tournament)
    ordinal_num   = models.SmallIntegerField()
    opening_time  = models.DateTimeField()
    closing_time  = models.DateTimeField()

    def __str__(self):
        return str(self.ordinal_num)

    class Meta:
        ordering = ["ordinal_num"]


class Fight(models.Model):

    # Python lacks proper enums and constants, so use these static
    # variables to refer to 'status' values from Python code.
    NOT_STARTED = 0
    IN_PROGRESS = 1
    COMPLETED   = 2

    _STATUS_CHOICES = [
        (NOT_STARTED, _tr("Not started")),
        (IN_PROGRESS, _tr("In progress")),
        (COMPLETED,   _tr("Completed"))]

    tournament    = models.ForeignKey(Tournament)
    round         = models.ForeignKey(TournamentRound)
    room          = models.ForeignKey(Room)
    start_time    = models.DateTimeField(null=True, blank=True)
    stop_time     = models.DateTimeField(null=True, blank=True)
    status        = models.PositiveSmallIntegerField(choices=_STATUS_CHOICES,
                                                     default=NOT_STARTED)
    team1         = models.ForeignKey(Team, related_name="+")
    team2         = models.ForeignKey(Team, related_name="+")
    team3         = models.ForeignKey(Team, related_name="+",
                                            null=True, blank=True)
    team4         = models.ForeignKey(Team, related_name="+",
                                            null=True, blank=True)
    jury          = models.ManyToManyField(Juror, blank=True)

    def clean(self):
        super().clean()

        bad = (self.start_time is not None and
               self.stop_time  is not None and
               self.start_time >= self.stop_time)
        if bad:
            msg = _tr("Fight is completed before being started")
            raise exceptions.ValidationError({"stop_time": msg})

        if self.team3 is None and self.team4 is not None:
            msg = _tr("Team 3 must be given when team 4 is given")
            raise exceptions.ValidationError({"team3": msg})

        teams = [self.team1, self.team2, self.team3, self.team4]
        teams_uniq = set(teams) - {None}

        # noinspection PyTypeChecker
        if len(teams_uniq) < 2 or len(teams_uniq) + teams.count(None) != 4:
            msg = _tr("Participating teams are not unique")
            raise exceptions.ValidationError(msg)

        tournaments_of_team = set([team.tournament for team in teams_uniq])
        if len(tournaments_of_team) > 1:
            msg = _tr('Teams belong to different tournaments!')
            raise exceptions.ValidationError(msg)

    def __str__(self):
        return _tr("{0} at {1}").format(self.round, self.room)

    class Meta:
        unique_together = ("room", "round")
        ordering  = ["round", "room"]


class FightStage(models.Model):
    fight         = models.ForeignKey(Fight)
    action_num    = models.IntegerField()
    problem       = models.ForeignKey(Problem)
    reporter      = models.ForeignKey(Participant, related_name="+")
    opponent      = models.ForeignKey(Participant, related_name="+")
    reviewer      = models.ForeignKey(Participant, related_name="+",
                                                   null=True, blank=True)

    def clean(self):
        super().clean()

        guys = [self.reporter, self.opponent, self.reviewer]
        guys_uniq = set(guys) - {None}

        # noinspection PyTypeChecker
        if len(guys_uniq) < 2 or len(guys_uniq) + guys.count(None) != 3:
            msg = _tr("Single person is assigned for two or more roles")
            raise exceptions.ValidationError(msg)

    def __str__(self):
        return 'Fight #{0}, stage #{1} at {2}'.format(
            self.fight.fight_num, self.action_num, self.fight.room.designation)

    class Meta:
        unique_together = ("fight", "action_num")


class Refusal(models.Model):
    tournament    = models.ForeignKey(Tournament)
    fight_stage   = models.ForeignKey(FightStage)
    problem       = models.ForeignKey(Problem)

    class Meta:
        unique_together = ("fight_stage", "problem")


class JurorPoints(models.Model):
    tournament    = models.ForeignKey(Tournament)
    fight_stage   = models.ForeignKey(FightStage)
    juror         = models.ForeignKey(Juror)
    reporter_mark = models.IntegerField(null=True, blank=True)
    opponent_mark = models.IntegerField(null=True, blank=True)
    reviewer_mark = models.IntegerField(null=True, blank=True)

    def clean(self):
        super().clean()

        # clean reviewer
        bad = (self.reviewer_mark is None and
               self.fight_stage.fight.team3 is not None)
        if bad:
            msg = _tr("Reviewer mark must be set, because there is "
                      "a reviewing team in this fight")
            raise exceptions.ValidationError({"reviewer_mark": msg})

        # clean jury
        jury_set = set(self.fight_stage.fight.jury.all())
        if self.juror not in jury_set:
            msg = _tr("Selected juror doesn't take part in the fight")
            raise exceptions.ValidationError({"juror": msg})

    class Meta:
        unique_together = ("fight_stage", "juror")

# ---


class UserProfile(models.Model):
    user          = models.OneToOneField(User, related_name='scifight_extra')
    tournament    = models.ForeignKey('Tournament', blank=True, null=True)
