from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse('This is index page')


def tournament(request, tournament_slug):
    return HttpResponse('This is tournament page')


def schedule(request, tournament_slug):
    return HttpResponse('This is schedule page')


def fight(request, tournament_slug, fight_id):
    return HttpResponse('This is fight  #%s page' % fight_id)


def rooms(request, tournament_slug):
    return HttpResponse('This is rooms page')


def room(request, tournament_slug, room_id):
    return HttpResponse('This is room  #%s page' % room_id)


def teams(request, tournament_slug):
    return HttpResponse('This is teams page')


def team(request, tournament_slug, team_id=None, team_slug=None):
    return HttpResponse('This is team  #%s %s page' % (team_id, team_slug))


def participants(request, tournament_slug):
    return HttpResponse('This is participants page')


def participant(request, tournament_slug, participant_id):
    return HttpResponse('This is participant  #%s page' % participant_id)


def leaders(request, tournament_slug):
    return HttpResponse('This is leaders page')


def leader(request, tournament_slug, leader_id):
    return HttpResponse('This is leader  #%s page' % leader_id)


def juries(request, tournament_slug):
    return HttpResponse('This is juries page')


def jury(request, tournament_slug, jury_id):
    return HttpResponse('This is jury  #%s page' % jury_id)


def problems(request, tournament_slug):
    return HttpResponse('This is problems page')


def problem(request, tournament_slug, problem_num):
    return HttpResponse('This is problem  #%s page' % problem_num)
