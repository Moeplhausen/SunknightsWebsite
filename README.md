# Important Note
The code I wrote (Moeplhausen), which is like 95% of the whole project (exluding libs), you may use as you see fit as long as you don't use it for commercial projects (that includes sites that earn money with ads). For the rest of the code, there is so far no license, which means you have to contact those contributors if you want to use it or remove it.



# Sun Knights Website
A website for the Sun Knights Diep Clan.


## Install Instructions

#### If you have bash
  1. bash install.sh

#### If you don't have bash
  1. pip3 install -r requirements.txt --user
  2. python manage.py migrate
  3. python manage.py loaddata fixture.json
  
  
## Run it (dev)
  1. python manage.py runserver
  
####OR
  1. bash run.sh
