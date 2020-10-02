
# Sun Knights Website
A website for the Sun Knights Diep Clan.


## License
https://creativecommons.org/licenses/by-nc/3.0/

## Install Instructions

#### If you have bash (Bash is a Unix shell and command language i.e. has been used as the default login shell for most Linux distributions and all releases of Apple's macOS )
  1. bash install.sh

#### If you don't have bash
  1. pip3 install -r requirements.txt --user
  2. python3 manage.py migrate
  3. python3 manage.py loaddata fixture.json
  
  
## Run it (dev)
  python3 manage.py runserver
        'OR'
  bash run.sh
