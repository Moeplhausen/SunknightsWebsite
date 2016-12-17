from django.conf.urls import url,include

from .views import views
from .views.api import roles,servers,users,user_roles
from rest_framework_bulk.routes import BulkRouter

router = BulkRouter(trailing_slash=False)
router.register(r'roles',roles.RolesViewSet)
router.register(r'servers',servers.ServersViewSet)
router.register(r'users',users.ClanUsersViewSet)
router.register(r'userroles',user_roles.UserRolesViewSet)

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^api/',include(router.urls))
]