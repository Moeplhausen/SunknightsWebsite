from .modeltestcase import ModelTestCase
from ....models.clan_user import ClanUserRoles


class ClanUserTest(ModelTestCase):
    def setUp(self):
        self.setUpBasics()

    def test_is_points_manager(self):
        self.assertTrue(self.basic_admin.is_points_manager, 'Admin should always be points manager')
        self.assertFalse(self.basic_user.is_points_manager, 'User should not be points manager')
        # now give basic user the points manager role
        ClanUserRoles.objects.create(role=self.basic_discord_points_manager, clan_user=self.basic_user)
        self.assertTrue(self.basic_user.is_points_manager, 'User should now be a points manager')
        self.assertFalse(self.basic_user.is_war_manager, 'User should not be a war manager')

    def test_is_war_manager(self):
        self.assertTrue(self.basic_admin.is_points_manager, 'Admin should always be war manager')
        self.assertFalse(self.basic_user.is_war_manager, 'User should not be war manager')
        # now give basic user the war manager role
        ClanUserRoles.objects.create(role=self.basic_discord_war_manager, clan_user=self.basic_user)
        self.assertTrue(self.basic_user.is_war_manager, 'User should now be a war manager')
        self.assertFalse(self.basic_user.is_points_manager, 'User should not be a points manager')
