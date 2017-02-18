from .modeltestcase import ModelTestCase, ClanUser
from ....models.guildfight import GuildFight, GuildFightParticipation
from ....models.clan_user import ClanUserRoles
from ....models.point_submission import BasicUserPointSubmission,OneOnOneFightSubmission


class SubmissionsTests(ModelTestCase):
    def setUp(self):
        self.setUpBasics()

    def test_user_point_submission(self):

        #Lets create two submissions
        submissions1 = BasicUserPointSubmission.objects.create(pointsinfo=self.basic_user.pointsinfo, points=5,
                                                               proof='proof', gamemode=self.basic_gamemode,
                                                               tank=self.basic_tank, score=1000)
        submissions2 = BasicUserPointSubmission.objects.create(pointsinfo=self.basic_user.pointsinfo, points=15,
                                                               proof='proof2', gamemode=self.basic_gamemode,
                                                               tank=self.basic_tank, score=2000)

        #save current points
        currentpoints=self.basic_user.total_points

        self.assertEqual(currentpoints,0)

        submissions1.accepted=True
        submissions1.decided=True
        submissions1.manager=self.basic_admin
        submissions1.save()

        #need to reload the object because of the signal savers
        self.basic_user=ClanUser.objects.get(id=self.basic_user.id)
        self.assertEqual(self.basic_user.total_points,currentpoints+submissions1.points)


        #revert the submission
        submissions1.decided=False
        submissions1.save()
        #and accept the other submission
        submissions2.manager=self.basic_admin
        submissions2.decided=True
        submissions2.accepted=True
        submissions2.save()

        #need to reload the object because of the signal savers
        self.basic_user=ClanUser.objects.get(id=self.basic_user.id)
        self.assertEqual(self.basic_user.total_points,currentpoints+submissions2.points)

    def test_user_point_submission_mastery_grant(self):

        #there should be no masteries recorded yet
        self.assertFalse(self.basic_user.masteries.exists())

        #Lets create a submission that should give us a tier3 mastery
        submissions1 = BasicUserPointSubmission.objects.create(pointsinfo=self.basic_user.pointsinfo, points=0,
                                                               proof='proof', gamemode=self.basic_gamemode,
                                                               tank=self.basic_tank, score=1000000)

        submissions1.manager=self.basic_admin
        submissions1.accepted=True
        submissions1.decided=True
        submissions1.save()

        #need to reload the object because of the signal savers
        self.basic_user=ClanUser.objects.get(id=self.basic_user.id)

        #there should be now a mastery recorded
        self.assertTrue(self.basic_user.masteries.exists())

        #1million points should have been enough to get a tier 3 mastery
        self.assertEqual(self.basic_user.masteries.first().tier,5)


    def test_one_to_one_submission(self):
            submissions1 = OneOnOneFightSubmission.objects.create(pointsinfo=self.basic_user.pointsinfo,
                                                                  points=5,
                                                                  proof="proof",
                                                                  pointsinfoloser=self.basic_user2.pointsinfo,
                                                                  pointsloser=3,
                                                                  manager=self.basic_admin)

            self.assertEqual(self.basic_user.total_points,0)
            self.assertEqual(self.basic_user2.total_points,0)

            submissions1.accepted=submissions1.decided=True
            submissions1.save()
            #need to reload the object because of the signal savers
            self.basic_user=ClanUser.objects.get(id=self.basic_user.id)
            self.basic_user2=ClanUser.objects.get(id=self.basic_user2.id)

            self.assertEqual(self.basic_user.total_points,5)
            self.assertEqual(self.basic_user2.total_points,3)


            #check that points get reverted
            submissions1.accepted=submissions1.decided=False
            submissions1.save()

            #need to reload the object because of the signal savers
            self.basic_user=ClanUser.objects.get(id=self.basic_user.id)
            self.basic_user2=ClanUser.objects.get(id=self.basic_user2.id)

            self.assertEqual(self.basic_user.total_points,0)
            self.assertEqual(self.basic_user2.total_points,0)






