#!/bin/bash
#!/bin/bash
pip3 install -r requirements.txt --user
python3 manage.py migrate
python3 manage.py loaddata fixture.json
