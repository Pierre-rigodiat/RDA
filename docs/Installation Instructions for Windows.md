# Windows Installation Instructions

## Prerequisites

### Python
1. Download python 2.7 for windows 32bits from https://www.python.org/download/
2. Add to PATH:

C:\Python27\
C:\Python27\Scripts

### Pip
We need pip to do the installation of the required dependencies.  pip requires setuptools and it has to be installed first, before pip can run: http://www.pip-installer.org/en/latest/installing.html 
```
$ python get-pip.py 
```

### (Optional) Virtual Environment
1. In a command prompt:
```
$ pip install virtualenvwrapper-win
```
2. Add environment variable
WORKON_HOME=%USERPROFILE%\Develop\Envs
3. In a command prompt:
```
$ mkdir %WORKON_HOME%
$ cd %WORKON_HOME%
$ mkvirtualenv mgi
```
4. To use the environment (the prompt will become mgi. You should always see the mgi prompt when installing new packages):
```
$ workon mgi
```

### MongoDB
1. Download from https://www.mongodb.com/download-center#community
2. Follow the instructions provided by MongoDB to install it

### Redis Server
1. Download from https://github.com/MSOpenTech/redis/releases
2. Run the msi


## Setup

### Configure MongoDB
Please follow general instructions provided in the file called "MongoDB Configuration".

### Install required python packages
If you are using a virtual environment, make sure it is activated before starting the installation. 
```
$ pip install -r docs\requirements.txt
```

## Run the software for the first time
1. Run mongodb (if not already running):
```
$ mongod --config /path/to/source/conf/mongodb.conf
```
2. Setup the database:
```bash
$ python manage.py migrate
$ python manage.py createsuperuser
# Answer yes to:
# You just installed Django's auth system, which means you don't have any superusers defined.
# Would you like to create one now? (yes/no): yes
```

## Run the software
1. Make sure Redis Server is running.
2. Run mongodb (if not already running):
```
$ mongod --config /path/to/source/conf/mongodb.conf
```
3. Run celery:
```
$ celery -A mgi worker -l info -Ofair --purge
```
4. Run the software:
```
$ cd path/to/source
$ python manage.py runserver --noreload
```
5. (Optional) Allow remote access:
```
$ python manage.py runserver 0.0.0.0:<port> --noreload
```

## Access
For the Homepage, Go to:  http://127.0.0.1:8000/

For the Admin Dashboard, Go to:  http://127.0.0.1:8000/admin/ 
