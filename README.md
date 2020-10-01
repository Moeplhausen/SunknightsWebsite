
# Sun Knights Website
A website for the Sun Knights Diep Clan.


## License
https://creativecommons.org/licenses/by-nc/3.0/

## Install Instructions (For Windows, Mac and Linux)

#### If you have bash (Mac or Linux)
  Download the source code (by clicking 'clone' and 'Download zip' above)
  Extract the downloaded file and navigate into the extracted folder.
  Open terminal there and enter - 
    ./install.sh
  Installation will be started.

#### If you don't have bash (on Windows)
  Make sure that python (version 3 or above) is installed and is added to your PATH variable.
  Download the source code (by clicking 'clone' and 'Download zip' above)
  Extract the downloaded file and navigate into the extracted folder.
  Open terminal there and enter - 
  1. pip3 install -r requirements.txt --user
  2. python3 manage.py migrate
  3. python3 manage.py loaddata fixture.json
  
  
## Run it (dev)
  1. python3 manage.py runserver
  
####OR
  1. bash run.sh
