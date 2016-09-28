from django.conf.urls import include, url
from scifight import views


tournament_urls = [
    url(r'^$',                                           views.tournament,   name='tournament'),
    url(r'^schedule/$',                                  views.schedule,     name='schedule'),
    url(r'^fight/(?P<fight_id>[0-9]+)/$',                views.fight,        name='fight'),
    url(r'^rooms/$',                                     views.rooms,        name='rooms'),
    url(r'^room/(?P<room_id>[0-9]+)/$',                  views.room,         name='room'),
    url(r'^teams/$',                                     views.teams,        name='teams'),
    url(r'^team/(?P<team_id>[0-9]+)/$',                  views.team,         name='team_id'),
    url(r'^team/(?P<team_slug>[\w_-]+)/$',               views.team,         name='team_slug'),
    url(r'^participants/$',                              views.participants, name='participants'),
    url(r'^participant/(?P<participant_id>[0-9]+)/$',    views.participant,  name='participant'),
    url(r'^leaders/$',                                   views.leaders,      name='leaders'),
    url(r'^leader/(?P<leader_id>[0-9]+)/$',              views.leader,       name='leader'),
    url(r'^jury/$',                                      views.jury,         name='jury'),
    url(r'^juror/(?P<jury_id>[0-9]+)/$',                 views.juror,        name='juror'),
    url(r'^problems/$',                                  views.problems,     name='problems'),
    url(r'^problem/(?P<problem_num>[0-9]+)/$',           views.problem,      name='problem'),
]

urlpatterns = [
    url(r'^(?P<tournament_slug>[\w_-]+)/',               include(tournament_urls, namespace='scifight')),
]

