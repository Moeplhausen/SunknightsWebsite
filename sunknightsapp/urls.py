from django.conf.urls import url,include
from django.contrib.auth.views import logout_then_login


from .views import views
from .views.api import roles,servers,users,user_roles,tournaments,fights,discord_roles
from rest_framework_bulk.routes import BulkRouter
from .views.oauth.views import OAuthCallbackDiscord,OAuthRedirectDiscord


router = BulkRouter(trailing_slash=False)
router.register(r'roles',roles.RolesViewSet)
router.register(r'servers',servers.ServersViewSet)
router.register(r'users',users.ClanUsersViewSet)
router.register(r'userroles',user_roles.UserRolesViewSet)
router.register(r'tournaments',tournaments.TournamentsViewSet)
router.register(r'tournamentsfightsconnectors',tournaments.TournamentsFightsConnectorViewSet)
router.register(r'guildfights', fights.GuildFightsViewSet)
router.register(r'discord_roles',discord_roles.DiscordRolesViewSet)

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^me',views.home,name='userview'),
    url(r'^leaderboard', views.leaderboard, name='leaderboard'),
    url(r'^api/',include(router.urls)),
    url(r'^ajaxhandler/',views.ajaxhandler, name='ajaxhandler'),
    url(r'^logout/$', logout_then_login, name='logout'),

    url(r'^accounts/login/(?P<provider>Discord)/$',
        OAuthRedirectDiscord.as_view(params={'scope': 'identify guilds'})),
    url(r'^accounts/login/(?P<provider>(\w|-)+)/$', OAuthRedirectDiscord.as_view(), name='allaccess-login'),
    url(r'^accounts/callback/(?P<provider>(\w|-)+)/$', OAuthCallbackDiscord.as_view(), name='allaccess-callback'),


]