from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from core.views import new_game, view_game, create_move

urlpatterns = patterns('',
    url(r'^$',
        new_game, name='home'),
    url(r'^new_game$',
        new_game, name='new_game'),
    url(r'^view_game/(?P<game_id>\d+)/$',
        view_game, name='view_game'),
    url(
        r'^create_move/(?P<game_id>\d+)/$',
        view=create_move, name='create_move'),

    url(r'^admin/', include(admin.site.urls)),
)
