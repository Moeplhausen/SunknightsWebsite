from django.test import TestCase
from ....models.clan_user import ClanUser
from ....models.discord_roles import DiscordRole,SunKnightsRole
from ....models.discord_server import DiscordServer
from ....models.diep_tank import DiepTank,DiepTankInheritance
from ....models.diep_gamemode import DiepGamemode


class ModelTestCase(TestCase):

    def setUpBasics(self):
        self.basic_admin=ClanUser.objects.create(discord_id=1,discord_nickname='Admin',is_superuser=True)
        self.basic_user=ClanUser.objects.create(discord_id=2,discord_nickname='TestUser')
        self.basic_user2=ClanUser.objects.create(discord_id=3,discord_nickname='TestUser2')

        self.basic_discord_server=DiscordServer.objects.create(discord_id=1,name="Test Server")
        self.basic_discord_points_manager=DiscordRole.objects.create(name='Points Manager',discord_server=self.basic_discord_server,discord_id=1,can_manage_points=True)
        self.basic_discord_war_manager=DiscordRole.objects.create(name='War Manager',discord_server=self.basic_discord_server,discord_id=2,can_manage_wars=True)
        self.basic_guild1=SunKnightsRole.objects.create(name='Aurora',discord_server=self.basic_discord_server,discord_id=3,is_clan_guild=True)
        self.basic_guild2=SunKnightsRole.objects.create(name='Panda Squad',discord_server=self.basic_discord_server,discord_id=4,is_clan_guild=True)
        self.basic_guild3=SunKnightsRole.objects.create(name='Test',discord_server=self.basic_discord_server,discord_id=5,is_clan_guild=True)
        self.basic_tank=DiepTank.objects.create(name="Basic Tank",tier=1)
        DiepTankInheritance.objects.create(me=self.basic_tank,parent=None)
        self.basic_tank_twin=DiepTank.objects.create(name="Twin",tier=2)
        DiepTankInheritance.objects.create(me=self.basic_tank_twin,parent=self.basic_tank)
        self.basic_tank_triple=DiepTank.objects.create(name="Triple Shot",tier=3)
        DiepTankInheritance.objects.create(me=self.basic_tank_triple,parent=self.basic_tank_twin)
        self.basic_tank_quad=DiepTank.objects.create(name="Quad Tank",tier=3)
        DiepTankInheritance.objects.create(me=self.basic_tank_quad,parent=self.basic_tank_twin)
        self.basic_tank_triplet=DiepTank.objects.create(name="Triplet",tier=4)
        DiepTankInheritance.objects.create(me=self.basic_tank_triplet,parent=self.basic_tank_triple)
        self.basic_tank_penta=DiepTank.objects.create(name="Penta Shot",tier=4)
        DiepTankInheritance.objects.create(me=self.basic_tank_penta,parent=self.basic_tank_triple)
        self.basic_tank_octo=DiepTank.objects.create(name="Octo tank",tier=4)
        DiepTankInheritance.objects.create(me=self.basic_tank_octo,parent=self.basic_tank_quad)


        self.basic_gamemode=DiepGamemode.objects.create(name="Test Gamemode")