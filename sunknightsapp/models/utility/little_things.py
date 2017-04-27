MASTERY_TIER_OPTIONS = (
    (1, 'Tier 1'),
    (2, 'Tier 2'),
    (3, 'Tier 3'),
    (4, 'Tier 4'),
    (5, 'Tier 5'),
)
MASTERY_TIER_POINTS = (
    (1, 'Tier 1', 200000, 5),
    (2, 'Tier 2', 350000, 15),
    (3, 'Tier 3', 500000, 30),
    (4, 'Tier 4', 750000, 50),
    (5, 'Tier 5', 1000000, 75),
)
QUEST_TIER_OPTIONS=(
    (1,'Tier 1'),
    (2,'Tier 2'),
    (3,'Tier 3'),
    (4,'Bonus'),
)

POINTS_TABLE=(
    (5000000,1500,1000,750),
    (4000000,1000,750,500),
    (3500000,750,500,350),
    (3000000,500,350,250),
    (2500000,350,250,200),
    (2000000,250,200,150),
    (1750000,200,150,125),
    (1500000,150,125,100),
    (1250000,125,100,75),
    (1000000,100,75,50),
    (800000,75,50,35),
    (650000,50,35,25),
    (500000,35,25,15),
    (400000,25,15,12),
    (300000,15,12,10),
    (250000,12,10,8),
    (200000,10,8,5),
    (150000,8,5,3),
    (100000,5,3,2),
    (50000,3,2,1),
)


ELO_K=40
ELO_DEFAULT=1000


def float_or_0(value):
    try:
        return float(value)
    except:
        return 0


def getPointsByScore(submission):
    score=submission.score
    opness=submission.tank.opness

    for points in POINTS_TABLE:
        if score>=points[0]:
            return points[opness]

    return 0


def getPointsByFight(won:bool):
    if won:
        return 5
    return 2


def manageElo(submission):
    from decimal import getcontext, Decimal
    # Set the precision.

    winner=submission.pointsinfo
    loser=submission.pointsinfoloser

    def expected_elo(player,otherPlayer):
        return 1.0/(1+10**((otherPlayer.elo-player.elo)/400))


    cur_winner_elo=winner.elo
    cur_loser_elo=loser.elo

    expect_winner=expected_elo(winner,loser)
    expect_loser=expected_elo(loser,winner)

    winner.elo=cur_winner_elo+ELO_K*(1-expect_winner)
    loser.elo=cur_loser_elo+ELO_K*(0-expect_loser)

    t=str((round(expect_winner,2)))

    submission.expected_outcome=Decimal(t)

    winner.save()
    loser.save()


    pass


def getMasteryRankByPoints(points):
    if (points >= MASTERY_TIER_POINTS[4][2]):
        return 5
    elif (points >= MASTERY_TIER_POINTS[3][2]):
        return 4
    elif (points >= MASTERY_TIER_POINTS[2][2]):
        return 3
    elif points >= MASTERY_TIER_POINTS[1][2]:
        return 2
    elif points >= MASTERY_TIER_POINTS[0][2]:
        return 1
    else:
        return 0