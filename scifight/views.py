from django.shortcuts import render, get_object_or_404
from django.http import Http404
from scifight import models

get_or_404 = get_object_or_404


def render_with_context(request, template, **context):
    return render(request, template, context)


def index(request):
    return render_with_context(request, 'scifight/index.html',
        tournaments = models.Tournament.objects.all(),
        title       = "Willcommen")


def tournament(request, tournament_slug):
    return render_with_context(request, 'scifight/tournament.html',
        tournament = get_or_404(models.Tournament, slug=tournament_slug))


def schedule(request, tournament_slug):
    tnmt = get_or_404(models.Tournament, slug=tournament_slug)
    return render_with_context(request, 'scifight/schedule.html',
        tournament      = tnmt,
        fights          = models.Fight.objects.filter(tournament=tnmt),
        nav_active_item = "schedule")


def fight(request, tournament_slug, fight_id):
    tnmt = get_or_404(models.Tournament, slug=tournament_slug)
    return render_with_context(request, 'scifight/fight.html',
        tournament      = tnmt,
        fight           = get_or_404(models.Fight, pk=fight_id, tournament=tnmt),
        nav_active_item = "schedule")


def rooms(request, tournament_slug):
    tnmt = get_or_404(models.Tournament, slug=tournament_slug)
    return render_with_context(request, 'scifight/rooms.html',
        tournament      = tnmt,
        rooms           = models.Room.objects.filter(tournament=tnmt),
        nav_active_item = "rooms")


def room(request, tournament_slug, room_id):
    tnmt = get_or_404(models.Tournament, slug=tournament_slug)
    return render_with_context(request, 'scifight/room.html',
        tournament      = tnmt,
        room            = get_or_404(models.Room, pk=room_id, tournament=tnmt),
        nav_active_item = "rooms")


def teams(request, tournament_slug):
    tnmt = get_or_404(models.Tournament, slug=tournament_slug)
    return render_with_context(request, 'scifight/teams.html',
        tournament      = tnmt,
        teams           = models.Team.objects.filter(tournament=tnmt),
        nav_active_item = "teams")


def team(request, tournament_slug, team_id=None, team_slug=None):
    tnmt = get_or_404(models.Tournament, slug=tournament_slug)

    if team_id:
        team = get_or_404(models.Team, pk=team_id, tournament=tnmt)
    elif team_slug:
        team = get_or_404(models.Team, slug=team_slug, tournament=tnmt)
    else:
        raise Http404()

    return render_with_context(request, 'scifight/team.html',
        tournament      = tnmt,
        team            = team,
        nav_active_item = "teams")


def participants(request, tournament_slug):
    tnmt = get_or_404(models.Tournament, slug=tournament_slug)
    return render_with_context(request, 'scifight/participants.html',
        tournament      = tnmt,
        participants    = models.Participant.objects.filter(tournament=tnmt),
        nav_active_item = "participant")


def participant(request, tournament_slug, participant_id):
    tnmt = get_or_404(models.Tournament, slug=tournament_slug)
    return render_with_context(request, 'scifight/participant.html',
        tournament      = tnmt,
        participant     = get_or_404(models.Participant,
                                     pk=participant_id, tournament=tnmt),
        nav_active_item = "participants")


def leaders(request, tournament_slug):
    tnmt = get_or_404(models.Tournament, slug=tournament_slug)
    return render_with_context(request, 'scifight/leaders.html',
        tournament      = tnmt,
        leaders         = tnmt.leader_set.all(),
        nav_active_item = "leaders")


def leader(request, tournament_slug, leader_id):
    tnmt   = get_or_404(models.Tournament, slug=tournament_slug)
    leader = get_or_404(models.Leader, pk=leader_id, tournament=tnmt)
    return render_with_context(request, 'scifight/leader.html',
        tournament      = tnmt,
        leader          = leader,
        nav_active_item = "leaders")


def jury(request, tournament_slug):
    tnmt = get_or_404(models.Tournament, slug=tournament_slug)
    return render_with_context(request, 'scifight/jury.html',
        tournament      = tnmt,
        jury            = models.Juror.objects.filter(tournament=tnmt),
        nav_active_item = "jury")


def juror(request, tournament_slug, jury_id):
    tnmt  = get_or_404(models.Tournament, slug=tournament_slug)
    juror = get_or_404(models.Juror, pk=jury_id, tournament=tnmt)
    return render_with_context(request, 'scifight/juror.html',
        tournament      = tnmt,
        juror           = juror,
        nav_active_item = "jury")


def problems(request, tournament_slug):
    tnmt     = get_or_404(models.Tournament, slug=tournament_slug)
    problems = models.Problem.objects.filter(tournament=tnmt)
    return render_with_context(request, 'scifight/problems.html',
        tournament      = tnmt,
        problems        = problems,
        nav_active_item = "problems")


def problem(request, tournament_slug, problem_num):
    tnmt    = get_or_404(models.Tournament, slug=tournament_slug)
    problem = get_or_404(models.Problem,
                         problem_num=problem_num, tournament=tnmt)
    return render_with_context(request, 'scifight/problem.html',
        tournament      = tnmt,
        problem         = problem,
        nav_active_item = "problem")
