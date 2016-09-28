from django.shortcuts import render, get_object_or_404
from django.http import Http404
from scifight import models


def index(request):
    tournaments = models.Tournament.objects.all()
    context = dict(tournaments=tournaments)
    return render(request, 'scifight/index.html', context)


def tournament(request, tournament_slug):
    tournament = get_object_or_404(models.Tournament, slug=tournament_slug)
    context = dict(tournament=tournament)
    return render(request, 'scifight/tournament.html', context)


def schedule(request, tournament_slug):
    fights = models.Fight.objects.filter(tournament__slug=tournament_slug)
    context = dict(fights=fights)
    return render(request, 'scifight/schedule.html', context)


def fight(request, tournament_slug, fight_id):
    fight = get_object_or_404(models.Fight, pk=fight_id,
                              tournament__slug=tournament_slug)
    jury = fight.jury.all()
    fightstages = fight.fightstage_set.all()
    context = dict(fight=fight,
                   jury=jury,
                   fightstages=fightstages)
    return render(request, 'scifight/fight.html', context)


def rooms(request, tournament_slug):
    rooms = models.Room.objects.filter(tournament__slug=tournament_slug)
    context = dict(rooms=rooms)
    return render(request, 'scifight/rooms.html', context)


def room(request, tournament_slug, room_id):
    room = get_object_or_404(models.Room, pk=room_id,
                             tournament__slug=tournament_slug)
    fights = room.fight_set.all()
    context = dict(room=room,
                   fights=fights)
    return render(request, 'scifight/room.html', context)


def teams(request, tournament_slug):
    teams = models.Team.objects.filter(tournament__slug=tournament_slug)
    context = dict(teams=teams)
    return render(request, 'scifight/teams.html', context)


def team(request, tournament_slug, team_id=None, team_slug=None):
    if team_id:
        team = get_object_or_404(models.Team, pk=team_id,
                                 tournament__slug=tournament_slug)
    elif team_slug:
        team = get_object_or_404(models.Team, slug=team_slug,
                                 tournament__slug=tournament_slug)
    else:
        Http404()
    participants = team.participant_set.all()
    leaders = team.leader_set.all()
    context = dict(team=team,
                   leaders=leaders,
                   participants=participants)
    return render(request, 'scifight/team.html', context)


def participants(request, tournament_slug):
    participants = models.Participant.objects.filter(
        tournament__slug=tournament_slug
    )
    context = dict(participants=participants)
    return render(request, 'scifight/participants.html', context)


def participant(request, tournament_slug, participant_id):
    participant = get_object_or_404(models.Participant, pk=participant_id,
                                    tournament__slug=tournament_slug)
    context = dict(participant=participant)
    return render(request, 'scifight/participant.html', context)


def leaders(request, tournament_slug):
    leaders = models.Leader.objects.filter(tournament__slug=tournament_slug)
    context = dict(leaders=leaders)
    return render(request, 'scifight/leaders.html', context)


def leader(request, tournament_slug, leader_id):
    leader = get_object_or_404(models.Leader, pk=leader_id,
                               tournament__slug=tournament_slug)
    contex = dict(leader=leader)
    return render(request, 'scifight/leader.html', contex)


def jury(request, tournament_slug):
    jury = models.Juror.objects.filter(tournament__slug=tournament_slug)
    context = dict(jury=jury)
    return render(request, 'scifight/jury.html', context)


def juror(request, tournament_slug, jury_id):
    juror = get_object_or_404(models.Juror, pk=jury_id,
                             tournament__slug=tournament_slug)
    context = dict(juror=juror)
    return render(request, 'scifight/juror.html', context)


def problems(request, tournament_slug):
    problems = models.Problem.objects.filter(tournament__slug=tournament_slug)
    context = dict(problems=problems)
    return render(request, 'scifight/problems.html', context)


def problem(request, tournament_slug, problem_num):
    problem = get_object_or_404(models.Problem, problem_num=problem_num,
                                tournament__slug=tournament_slug)
    context = dict(problem=problem)
    return render(request, 'scifight/problem.html', context)
