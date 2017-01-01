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


def getMasteryRankByPoints(points):
    if (points >= MASTERY_TIER_POINTS[2][2]):
        return 3
    elif points >= MASTERY_TIER_POINTS[1][2]:
        return 2
    elif points >= MASTERY_TIER_POINTS[0][2]:
        return 1
    else:
        return 0