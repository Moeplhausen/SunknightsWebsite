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
    ├── backgroundTask/     
        ├── __init__.py
        └── webhook_spam.py
    ├── decorators/   
        ├── __init__.py
        └── login_decorators.py
        
        
```
