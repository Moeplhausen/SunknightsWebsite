from django.conf import settings
import requests

redcolor = 16711680
greencolor = 65280
yellowcolor = 16776960
orangecolor = 16753920


def post_to_discord(dictdata):
    url = settings.POINTSWEBHOOK
    data = dictdata
    if not settings.TESTING:
        r = requests.post(url, json=data)
    else:
        pass
        # print(data)


def post_new_guild_fight(fight):
    data = {'embeds':
        [
            {
                'color': yellowcolor,
                'fields':
                    [
                        {'name': 'New GuildFight (id={})'.format(fight.id), 'value': fight.name, 'inline': True},
                        {'name': 'Date', 'value': str(fight.date), 'inline': True},
                        {'name': 'Guild 1', 'value': '<@{}>'.format(fight.team1.discord_id), 'inline': True},
                        {'name': 'Guild 2', 'value': '<@{}>'.format(fight.team2.discord_id), 'inline': True},
                    ]
            }
        ]
    }
    post_to_discord(data)


def post_submission_reverted(submission):
    data = {}
    data = {'embeds':
        [
            {
                'color': orangecolor,
                'title': 'Submission Reverted ({})'.format(submission.id),
                'thumbnail':{'url':submission.pointsinfo.user.avatar_url},
                'fields':
                    [
                        {'name': 'From', 'value': '<@{}>'.format(submission.pointsinfo.user.discord_id), 'inline': True},
                        {'name': 'Manager', 'value': '<@'+str(submission.manager.discord_id)+'>', 'inline': True},
                        {'name': 'Points', 'value': str(submission.points), 'inline': True},

                    ]
            }
        ]
    }


    post_to_discord(data)


def post_guild_fight_results(fight):
    data = {'embeds':
        [
            {
                'color': greencolor,
                'fields':
                    [
                        {'name': 'GuildFight results (id={})'.format(fight.id), 'value': fight.name, 'inline': True},
                        {'name': 'Date', 'value': str(fight.date), 'inline': True},
                        {'name': 'winner', 'value': '<@{}>'.format(fight.winner.discord_id), 'inline': True},
                        {'name': 'loser', 'value': '<@{}>'.format(fight.loser.discord_id), 'inline': True},
                    ]
            }
        ]
    }
    post_to_discord(data)


def post_new_user_point_submission(submission, accepted, decided):
    data = {}
    if not decided:
        data = {'embeds':
            [
                {
                    'color': yellowcolor,
                    'title': 'New Point Submission ({})'.format(submission.id),
                    'thumbnail':{'url':submission.pointsinfo.user.avatar_url},
                    'fields':
                        [
                            {'name': 'From', 'value': '<@{}>'.format(submission.pointsinfo.user.discord_id), 'inline': True},
                            {'name': 'Score', 'value': str(submission.score), 'inline': True},
                            {'name': 'Tank', 'value': submission.tank.name, 'inline': True},
                            {'name': 'Expected Points', 'value': str(submission.points), 'inline': True},
                            {'name': 'Proof', 'value': submission.proof, 'inline': True},
                            {'name': 'Note', 'value': submission.submitterText, 'inline': True},
                        ]
                }
            ]
        }
    else:
        data = {'embeds':
            [
                {
                    'color': greencolor if accepted else redcolor,
                    'title': 'Submission ({})'.format(submission.id),
                    'thumbnail':{'url':submission.pointsinfo.user.avatar_url},
                    'fields':
                        [
                            {'name': 'From', 'value': '<@{}>'.format(submission.pointsinfo.user.discord_id), 'inline': True},
                            {'name': 'Submitter Note', 'value': submission.submitterText, 'inline': True},
                            {'name': 'Action', 'value': 'Approved' if accepted else 'Rejected', 'inline': True},
                            {'name': 'Manager', 'value': '<@{}>'.format(submission.manager.discord_id), 'inline': True},
                            {'name': 'Manager Note', 'value': submission.managerText, 'inline': True},
                            {'name': 'Score', 'value': str(submission.score), 'inline': True},
                            {'name': 'Points', 'value': str(submission.points), 'inline': True},
                            {'name': 'Proof', 'value': submission.proof, 'inline': True},
                        ]
                }
            ]
        }
    print(data)
    post_to_discord(data)



def post_new_event_quest_submission(submission, accepted, decided):
    data = {}
    if not decided:
        data = {'embeds':
            [
                {
                    'color': yellowcolor,
                    'title': 'New Event/Quest Submission ({})'.format(submission.id),
                    'thumbnail':{'url':submission.pointsinfo.user.avatar_url},
                    'fields':
                        [
                            {'name': 'From', 'value': '<@{}>'.format(submission.pointsinfo.user.discord_id), 'inline': True},
                            {'name': 'Proof', 'value': submission.proof, 'inline': True},
                            {'name': 'Note', 'value': submission.submitterText, 'inline': True},
                            {'name':'Quest','value':("T"+str(submission.questtask.tier)+": "+submission.questtask.questtext) if submission.questtask else "None",'inline':True}
                        ]
                }
            ]
        }
    else:
        data = {'embeds':
            [
                {
                    'color': greencolor if accepted else redcolor,
                    'title': 'Submission ({})'.format(submission.id),
                    'thumbnail':{'url':submission.pointsinfo.user.avatar_url},
                    'fields':
                        [
                            {'name': 'From', 'value': '<@{}>'.format(submission.pointsinfo.user.discord_id), 'inline': True},
                            {'name': 'Submitter Note', 'value': submission.submitterText, 'inline': True},
                            {'name': 'Action', 'value': 'Approved' if accepted else 'Rejected', 'inline': True},
                            {'name': 'Manager', 'value': '<@{}>'.format(submission.manager.discord_id), 'inline': True},
                            {'name': 'Manager Note', 'value': submission.managerText, 'inline': True},
                            {'name': 'Points', 'value': str(submission.points), 'inline': True},
                            {'name': 'Proof', 'value': submission.proof, 'inline': True},
                            {'name':'Quest','value':("T"+str(submission.questtask.tier)+": "+submission.questtask.questtext) if submission.questtask else "None",'inline':True}
                        ]
                }
            ]
        }
    print(data)
    post_to_discord(data)







def post_new_submission(submission, accepted, decided):
    data = {}
    if not decided:
        data = {'embeds':
            [
                {
                    'color': yellowcolor,
                    'title': 'New Submission ({})'.format(submission.id),
                    'thumbnail':{'url':submission.pointsinfo.user.avatar_url},
                    'fields':
                        [
                            {'name': 'From', 'value': submission.pointsinfo.user.discord_nickname, 'inline': True},
                        ]
                }
            ]
        }
    else:
        data = {'embeds':
            [
                {
                    'color': greencolor if accepted else redcolor,
                    'title': 'Submission ({})'.format(submission.id),
                    'thumbnail':{'url':submission.pointsinfo.user.avatar_url},
                    'fields':
                        [
                            {'name': 'From', 'value': submission.pointsinfo.user.discord_nickname, 'inline': True},
                            {'name': 'Action', 'value': 'Approved' if accepted else 'Rejected', 'inline': True},
                        ]
                }
            ]
        }
    print(data)
    post_to_discord(data)


def post_new_OneOnOne_submission(submission, accepted, decided):
    data = {}
    if not decided:
        data = {'embeds':
            [
                {
                    'color': yellowcolor,
                    'title': 'New One on One Submission ({})'.format(submission.id),
                    'fields':
                        [
                            {'name': 'Winner', 'value': '<@{}>'.format(submission.pointsinfo.user.discord_id), 'inline': True},
                            {'name': 'Loser', 'value': '<@{}>'.format(submission.pointsinfoloser.user.discord_id), 'inline': True},
                            {'name': 'Points Winner', 'value': str(submission.points), 'inline': True},
                            {'name': 'Points Loser', 'value': str(submission.pointsloser), 'inline': True},
                            {'name': 'Proof', 'value': submission.proof, 'inline': False},
                        ]
                }
            ]
        }
    else:
        data = {'embeds':
            [
                {
                    'color': greencolor if accepted else redcolor,
                    'title': 'One on One Fight Submission ({})'.format(submission.id),
                    'fields':
                        [
                            {'name': 'Winner', 'value': '<@{}>'.format(submission.pointsinfo.user.discord_id), 'inline': True},
                            {'name': 'Loser', 'value': '<@{}>'.format(submission.pointsinfoloser.user.discord_id), 'inline': True},
                            {'name': 'Manager', 'value': '<@{}>'.format(submission.manager.discord_id), 'inline': True},
                            {'name': 'Manager Note', 'value': submission.managerText, 'inline': True},
                            {'name': 'Action', 'value': 'Approved' if accepted else 'Rejected', 'inline': True},
                            {'name': 'Expected outcome', 'value': str(submission.expected_outcome), 'inline': True},
                            {'name': 'Proof', 'value': submission.proof, 'inline': True},
                        ]
                }
            ]
        }
    print(data)
    post_to_discord(data)


def post_new_manager_submission(submission, accepted):
    if accepted:
        data = {'embeds':
            [
                {
                    'color': greencolor,
                    'title': 'Custom Points action ({})'.format(submission.id),
                    'thumbnail':{'url':submission.pointsinfo.user.avatar_url},
                    'fields':
                        [
                            {'name': 'Member', 'value': '<@{}>'.format(submission.pointsinfo.user.discord_id), 'inline': True},
                            {'name': 'Action', 'value': 'Addition' if submission.points >= 0 else 'Subtraction',
                             'inline': True},
                            {'name': 'Points', 'value': str(submission.points), 'inline': True},
                            {'name': 'Points Total', 'value': str(submission.pointsinfo.totalpoints), 'inline': True},
                            {'name': 'Manager', 'value': '<@{}>'.format(submission.manager.discord_id), 'inline': True},
                            {'name': 'Manager Note', 'value': submission.managerText, 'inline': True},
                        ]
                }
            ]
        }
    else:
        data = {'embeds':
            [
                {
                    'color': redcolor,
                    'title': 'Custom Points action ({})'.format(submission.id),
                    'thumbnail':{'url':submission.pointsinfo.user.avatar_url},
                    'fields':
                        [
                            {'name': 'Member', 'value': '<@{}>'.format(submission.pointsinfo.user.discord_id), 'inline': True},
                            {'name': 'Action', 'value': 'Reverted', 'inline': True},
                        ]
                }
            ]
        }
    post_to_discord(data)


def post_new_guildfight_points(submission, accepted):
    data = {}
    if accepted:
        data = {'embeds':
            [
                {
                    'color': greencolor,
                    'title': 'Guild fight points ({})'.format(submission.id),
                    'fields':
                        [
                            {'name': 'Member', 'value': '<@{}>'.format(submission.pointsinfo.user.discord_id), 'inline': True},
                            {'name': 'Action', 'value': 'Addition' if submission.points >= 0 else 'Subtraction',
                             'inline': True},
                            {'name': 'Points', 'value': str(submission.points), 'inline': True},
                            {'name': 'Manager Note', 'value': submission.managerText, 'inline': True},
                        ]
                }
            ]
        }
    else:
        data = {'embeds':
            [
                {
                    'color': redcolor,
                    'title': 'Custom Points action ({})'.format(submission.id),
                    'fields':
                        [
                            {'name': 'Member', 'value': '<@{}>'.format(submission.pointsinfo.user.discord_id), 'inline': True},
                            {'name': 'Action', 'value': 'Reverted', 'inline': True},
                        ]
                }
            ]
        }
    post_to_discord(data)


def mastery_unlock(mastery):
    data = {'embeds':
        [
            {
                'color': greencolor,
                'title': 'Mastery Unlock',
                'thumbnail':{'url':mastery.pointsinfo.user.avatar_url},
                'fields':
                    [
                        {'name': 'Member', 'value': '<@{}>'.format(mastery.pointsinfo.user.discord_id), 'inline': True},
                        {'name': 'Tank', 'value': mastery.tank.name, 'inline': True},
                        {'name': 'Tier', 'value': str(mastery.tier), 'inline': True},
                        {'name': 'Manager', 'value': '<@{}>'.format(mastery.manager.discord_id), 'inline': True},
                    ]
            }
        ]
    }

    post_to_discord(data)
