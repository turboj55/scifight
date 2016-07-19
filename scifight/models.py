from django.db import models

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


class TeamOrigin(models.Model):
    name = models.CharField(max_length=NAME_LENGTH)

    def __str__(self):
        return self.name


class Team(models.Model):
    name = models.CharField(max_length=NAME_LENGTH)
    description = models.TextField(max_length=TEXT_LENGTH, blank=True)
    origin = models.ForeignKey(TeamOrigin, null=True, blank=True)

    def __str__(self):
        return self.name


class CommonOrigin(models.Model):
    name = models.CharField(max_length=NAME_LENGTH)

    def __str__(self):
        return self.name


class Participant(models.Model):
    short_name  = models.CharField(max_length=NAME_LENGTH)
    full_name   = models.CharField(max_length=NAME_LENGTH, blank=True)
    origin      = models.ForeignKey(CommonOrigin, null=True, blank=True)
    grade       = models.CharField(max_length=GRADE_LENGTH, blank=True)
    team        = models.ForeignKey(Team)
    is_capitan  = models.BooleanField()

    def __str__(self):
        return self.short_name


class Leader(models.Model):
    short_name  = models.CharField(max_length=NAME_LENGTH)
    full_name   = models.CharField(max_length=NAME_LENGTH, blank=True)
    origin      = models.ForeignKey(CommonOrigin, null=True, blank=True)

    def __str__(self):
        return self.short_name


class Jury(models.Model):
    short_name  = models.CharField(max_length=NAME_LENGTH)
    full_name   = models.CharField(max_length=NAME_LENGTH, blank=True)
    origin      = models.ForeignKey(CommonOrigin)

    def __str__(self):
        return self.short_name


class Room(models.Model):
    name        = models.CharField(max_length=NAME_LENGTH)

    def __str__(self):
        return self.name


class Problem(models.Model):
    problem_num = models.IntegerField(primary_key=True)
    name        = models.CharField(max_length=NAME_LENGTH)
    description = models.TextField(max_length=TEXT_LENGTH, blank=True)

    def __str__(self):
        return "#{0}. {1}".format(self.problem_num, self.name)


class JuryPoints(models.Model):
    jury          = models.ForeignKey(Jury)
    reporter_mark = models.IntegerField()
    opponent_mark = models.IntegerField()
    reviewer_mark = models.IntegerField(null=True, blank=True)


class FightStage(models.Model):
    action_num  = models.IntegerField()
    problem     = models.ForeignKey(Problem)
    reporter    = models.ForeignKey(Participant, related_name="reporter")
    opponent    = models.ForeignKey(Participant, related_name="opponent")
    reviewer    = models.ForeignKey(Participant, related_name="reviewer", null=True, blank=True)
    refusals    = models.ManyToManyField(Problem, related_name="refusals")
    points      = models.ManyToManyField(JuryPoints)


class Fight(models.Model):
    room        = models.ForeignKey(Room)
    fight_num   = models.IntegerField()
    start_time  = models.DateTimeField(null=True, blank=True)
    stop_time   = models.DateTimeField(null=True, blank=True)
    status      = models.PositiveSmallIntegerField(default=0)
    team1       = models.ForeignKey(Team, related_name="team1")
    team2       = models.ForeignKey(Team, related_name="team2")
    team3       = models.ForeignKey(Team, related_name="team3", null=True, blank=True)
    team4       = models.ForeignKey(Team, related_name="team4", null=True, blank=True)
    juries      = models.ManyToManyField(Jury)
    stages      = models.ManyToManyField(FightStage)
