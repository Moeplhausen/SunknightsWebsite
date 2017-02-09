MASTERY_TIER_OPTIONS = (
    (1, 'Tier 1'),
    (2, 'Tier 2'),
    (3, 'Tier 3'),
)
MASTERY_TIER_POINTS = (
    (1, 'Tier 1', 200000, 5),
    (2, 'Tier 2', 350000, 15),
    (3, 'Tier 3', 500000, 30),
)
QUEST_TIER_OPTIONS=(
    (1,'Tier 1'),
    (2,'Tier 2'),
    (3,'Tier 3'),
    (4,'Bonus'),
)

ELO_K=40
ELO_DEFAULT=1000


def getPointsByScore(score:int):
    return round(score/100000.0,1)


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
    if (points >= MASTERY_TIER_POINTS[2][2]):
        return 3
    elif points >= MASTERY_TIER_POINTS[1][2]:
        return 2
    elif points >= MASTERY_TIER_POINTS[0][2]:
        return 1
    else:
        return 0