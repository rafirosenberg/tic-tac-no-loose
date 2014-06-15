from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from core.views import view_game, create_move

urlpatterns = patterns('',
    url(r'^view_game/(?P<game_id>\d+)/$',
        view_game, name='view_game'),
    url(
        r'^create_move/(?P<game_id>\d+)/$',
        view=create_move, name='create_move'),
    url(r'^admin/', include(admin.site.urls)),
)
