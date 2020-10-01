[![forthebadge](https://forthebadge.com/images/badges/built-by-developers.svg)](https://github.com/Moeplhausen/SunknightsWebsite)
[![forthebadge](https://forthebadge.com/images/badges/built-with-love.svg)](https://github.com/Moeplhausen/SunknightsWebsite)
[![forthebadge](https://forthebadge.com/images/badges/contains-technical-debt.svg)](https://github.com/Moeplhausen/SunknightsWebsite)
[![forthebadge](https://forthebadge.com/images/badges/fixed-bugs.svg)](https://github.com/Moeplhausen/SunknightsWebsite)
[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://github.com/Moeplhausen/SunknightsWebsite)
[![forthebadge](https://forthebadge.com/images/badges/uses-js.svg)](https://github.com/Moeplhausen/SunknightsWebsite)
[![forthebadge](https://forthebadge.com/images/badges/uses-html.svg)](https://github.com/Moeplhausen/SunknightsWebsite)
[![forthebadge](https://forthebadge.com/images/badges/uses-css.svg)](https://github.com/Moeplhausen/SunknightsWebsite)
[![forthebadge](https://forthebadge.com/images/badges/open-source.svg)](https://github.com/Moeplhausen/SunknightsWebsite)

# Sun Knights Website
A website for the Sun Knights Diep Clan.


## License
https://creativecommons.org/licenses/by-nc/3.0/

## Install Instructions

#### If you have bash
  1. bash install.sh

#### If you don't have bash
  1. pip3 install -r requirements.txt --user
  2. python3 manage.py migrate
  3. python3 manage.py loaddata fixture.json
  
  
## Run it (dev)
  1. python3 manage.py runserver
  
####OR
  1. bash run.sh

## Structure

```bash
├── manage.py
├── fixture.json
├── README.md               # This file
├── sunknights.sql.zip
├── install.sh
├── installrun.sh
├── license
├── requirements.txt
├── run.sh
├── geoip/                    
    └── README.txt
├── sunknights/
    ├── __init__.py
    ├── settings.py
    ├── urls.py
    └── wsgi.py
└── sunknightsapp/
    ├── backgroundTask/     
        ├── __init__.py
        └── webhook_spam.py
    ├── decorators/   
        ├── __init__.py
        └── login_decorators.py
    
    ├── enums/     
        ├── __init__.py
        └── AjaxActions.py
    ├── forms/     
        ├── __init__.py
        ├── base_form.py
        ├── daily_quests_forms.py
        ├── fight_forms.py
        ├── misc_forms.py
        ├── points_forms.py
        ├── preferences_forms.py
        └── tournaments_forms.py
    ├── managers/     
        ├── __init__.py
        └── user_manager.py
    ├── middleware/     
        ├── __init__.py
        └── StrictAuthentication.py
    ├── models/     
        ├── __init__.py
        ├── clan_user.py
        ├── daily_quest.py
        ├── diep_gamemode.py
        ├── diep_tank.py
        ├── discord_role_points.py
        ├── discord_roles.py
        ├── discord_server.py
        ├── guildfight.py
        ├── help_info.py
        ├── mastery.py
        ├── point_submission.py
        ├── points_info.py
        ├── tournament.py
        └── utility/
            ├── __init__.py
            ├── children_save_finder.py
            └── little_things.py
    ├── processors/     
        ├── __init__.py
        └── context_processors.py
    ├── receivers/     
        ├── __init__.py
        └── user_created.py
    ├── serializers/     
        ├── __init__.py
        ├── clan_user_roles_serializer.py
        ├── clan_user_serializer.py
        ├── daily_quest_serializer.py
        ├── discord_mee6_points_serializer.py
        ├── discord_roles_serializer.py
        ├── discord_server_serializer.py
        ├── fight_serializer.py
        ├── gamemode_serializer.py
        ├── guild_fight_participant_serializer.py 
        ├── mastery_serializer.py
        ├── pointsubmissions_serializer.py 
        ├── tank_serializer.py
        └── tournament_serializer.py
```
