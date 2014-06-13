from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from core.views import create_move, view_game,

urlpatterns = patterns('',
    url(r'^create_move/(?P<game_id>\d+)/$', 
        'tictactoe.views.create_move', name='create_move'),
    url(r'^view_game/(?P<game_id>\d+)/$',
        'tictactoe.views.view_game', name='view_game'),

    url(r'^admin/', include(admin.site.urls)),
)
