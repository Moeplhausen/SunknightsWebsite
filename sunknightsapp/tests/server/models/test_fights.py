from .modeltestcase import ModelTestCase,ClanUser
from ....models.guildfight import GuildFight,GuildFightParticipation
from ....models.clan_user import ClanUserRoles

class FightTest(ModelTestCase):
    def setUp(self):
        self.setUpBasics()

    def createClanUserRoles(self):
        ClanUserRoles.objects.create(role=self.basic_guild1, clan_user=self.basic_user)

    def createBasicFights(self):
        self.fight1=GuildFight.objects.create(team1=self.basic_guild1,team2=self.basic_guild2,status=1,manager=self.basic_admin)
        self.fight2=GuildFight.objects.create(team1=self.basic_guild3,team2=self.basic_guild2,status=1,manager=self.basic_admin)




    def test_find_fights(self):
        #make user member of guild1
        self.createClanUserRoles()

        #user shouldn't find any fights yet
        self.assertFalse(self.basic_user.open_fights.exists())
        self.assertFalse(self.basic_user.finished_fights.exists())

        #now create a fight which user should see and one it shouldn't see because guild1 doesn't fight in it
        self.createBasicFights()

        #there are no finished fights
        self.assertFalse(self.basic_user.finished_fights.exists())

        #there should be one found fight
        self.assertEqual(self.basic_user.open_fights.count(),1)

        #now lets end fight2
        self.fight2.status=2
        #there still should be no finished fights found
        self.assertFalse(self.basic_user.finished_fights.exists())

        #now lets end fight1
        self.fight1.status=2
        self.fight1.save()

        #there should be a finished fights found now
        self.assertTrue(self.basic_user.finished_fights.exists())


    def test_fight_points(self):
        #save current points
        currentpoints=self.basic_user.total_points

        self.assertEqual(currentpoints,0)

        self.createBasicFights()
        self.createClanUserRoles()

        #there should be one found fight
        self.assertEqual(self.basic_user.open_fights.count(),1)


        #add basic user as a fight participant
        GuildFightParticipation.objects.create(fight=self.fight1,user=self.basic_user,tank=self.basic_tank,guild=self.basic_guild1)
        #There should be a team1 participant (basic user)
        self.assertTrue(self.fight1.team1fightparticipants.exists())


        self.fight1.status=2 #team1 won
        self.fight1.save()

        #need to reload the object because of the signal savers
        self.basic_user=ClanUser.objects.get(id=self.basic_user.id)

        #There should be a winner participant (basic user)
        self.assertTrue(self.fight1.winnerparticipants.exists())

        #basic user should have been granted fights for winning the fight
        self.assertEqual(self.basic_user.total_points,currentpoints+self.fight1.pointswinner)

        #now let us test that points are reverted when fight is not finished anymore
        self.fight1.status=1 #not finished
        self.fight1.save()

        #need to reload the object because of the signal savers
        self.basic_user=ClanUser.objects.get(id=self.basic_user.id)
        self.assertEqual(self.basic_user.total_points,0)



    def test_available_tanks_rules_1(self):#no rules
        self.createBasicFights()
        self.createClanUserRoles()

        self.fight1.rules=1
        participation=GuildFightParticipation.objects.create(fight=self.fight1,user=self.basic_user,tank=self.basic_tank_octo,guild=self.basic_guild1)

        #every tank is allowed. We should get them all
        self.assertEqual(self.fight1.available_tanks_team1.count(),7)


    def test_available_tanks_rules_2(self):#only level 45 tanks allowed and the parent tank (level 30) is banned for other level 45 tanks
        self.createBasicFights()
        self.createClanUserRoles()

        self.fight1.rules=2
        participation=GuildFightParticipation.objects.create(fight=self.fight1,user=self.basic_user,tank=self.basic_tank_octo,guild=self.basic_guild1)

        #There are only 3 level 45 tanks registered. Octo inherits from quad shot. So only Penta and Triplet should come up now
        self.assertEqual(self.fight1.available_tanks_team1.count(),2)

        #change tank to penta, only octo should come as option then
        participation.tank=self.basic_tank_penta
        participation.save()
        self.assertEqual(self.fight1.available_tanks_team1.count(),1)


    def test_available_tanks_rules_3(self):#unique lvl 45 tanks
        self.createBasicFights()
        self.createClanUserRoles()

        self.fight1.rules=3
        participation=GuildFightParticipation.objects.create(fight=self.fight1,user=self.basic_user,tank=self.basic_tank_octo,guild=self.basic_guild1)

        #There are only 3 level 45 tanks registered. Octo inherits from quad shot. So only Penta and Triplet should come up now
        self.assertEqual(self.fight1.available_tanks_team1.count(),2)

        #change tank to penta, only octo and triplet should come as option then
        participation.tank=self.basic_tank_penta
        participation.save()
        self.assertEqual(self.fight1.available_tanks_team1.count(),2)



    def test_available_tanks_rules_4(self):#only lvl 45 tanks
        self.createBasicFights()
        self.createClanUserRoles()

        self.fight1.rules=4
        participation=GuildFightParticipation.objects.create(fight=self.fight1,user=self.basic_user,tank=self.basic_tank_octo,guild=self.basic_guild1)

        #There are only 3 level 45 tanks registered. So only Penta, Octo and Triplet should come up now
        self.assertEqual(self.fight1.available_tanks_team1.count(),3)












