
# Sun Knights Website
A website for the Sun Knights Diep Clan.


## License
https://creativecommons.org/licenses/by-nc/3.0/

## Install Instructions

#### If you have bash
  1. bash install.sh
#### Bash Installation for linux
  1  sudo apt update
  2  sudo apt install bash-completion

#### If you don't have bash
  1. pip3 install -r requirements.txt --user
  2. python3 manage.py migrate
  3. python3 manage.py loaddata fixture.json
  
  
## Run it (dev)
  1. python3 manage.py runserver
  
####OR
  1. bash run.sh
