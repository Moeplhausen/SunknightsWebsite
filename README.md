
# Sun Knights Website
A website for the Sun Knights Diep Clan.


## License
https://creativecommons.org/licenses/by-nc/3.0/

## Install Instructions

#### If you have bash:
   
   bash [install.sh](https://github.com/manas1410/SunknightsWebsite/blob/master/install.sh)

#### If you don't have bash
  ```1. pip3 install -r requirements.txt --user```
  
  2. python3 [manage.py](https://github.com/manas1410/SunknightsWebsite/blob/master/manage.py) migrate
  
  3. python3 [manage.py](https://github.com/manas1410/SunknightsWebsite/blob/master/manage.py) loaddata [fixture.json](https://github.com/manas1410/SunknightsWebsite/blob/master/fixture.json)
  
  
## Run it (dev)
  python3 [manage.py](https://github.com/manas1410/SunknightsWebsite/blob/master/manage.py) runserver
  
#### OR
  bash [run.sh](https://github.com/manas1410/SunknightsWebsite/blob/master/run.sh)
