from django.conf.urls import url,include
from django.contrib.auth.views import logout_then_login


from .views import views
from .views.api import roles,servers,users,user_roles
from rest_framework_bulk.routes import BulkRouter
from .views.oauth.views import OAuthCallbackDiscord,OAuthRedirectDiscord


router = BulkRouter(trailing_slash=False)
router.register(r'roles',roles.RolesViewSet)
router.register(r'servers',servers.ServersViewSet)
router.register(r'users',users.ClanUsersViewSet)
router.register(r'userroles',user_roles.UserRolesViewSet)

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^me',views.home,name='userview'),
    url(r'^api/',include(router.urls)),
    url(r'^logout/$', logout_then_login, name='logout'),

    url(r'^accounts/login/(?P<provider>Discord)/$',
        OAuthRedirectDiscord.as_view(params={'scope': 'identify'})),
    url(r'^accounts/login/(?P<provider>(\w|-)+)/$', OAuthRedirectDiscord.as_view(), name='allaccess-login'),
    url(r'^accounts/callback/(?P<provider>(\w|-)+)/$', OAuthCallbackDiscord.as_view(), name='allaccess-callback'),


]