#!/bin/bash
MONGO_PORT=27017
DJANGO_PORT=8000
PROJ='mgi'
PYTHON='python'
CELERY='celery'
MONGO='mongod'

usage()
{
        echo "  ---------------------------------------------------------------------"
	echo " | launch_server_unix [options]                                      |"
	echo " |                                                                     |"
	echo " |       Options:                                                      |"
	echo " |                                                                     |"
	echo " |  -p  | --dir   : path to the django project (mandatory)             |"
	echo " |  -d  | --dport : django server port (8000 if not specified)         |"
	echo " |  -c  | --mconf : path to mongoDB configuration (mandatory)          |"
	echo " |  -m  | --mport : mongoDB port (27017 if not specified)              |"
	echo " |  -y  | --py    : path to python (not mandatory if path configured)  |"
	echo " |  -l  | --ce    : path to celery (not mandatory if path configured)  |"
	echo " |  -g  | --mo    : path to mongoDB (not mandatory if path configured) |"
	echo " |  -h  | --help  : help                                               |"
	echo " |                                                                     |"
	echo "  ---------------------------------------------------------------------"
	exit -1;
}


# Check if there is no argument
if [[ -z $* ]]; then
	echo 'No argument found. This is how you can use this script:'
	usage;
fi

# Check if there is -h or --help argument
for arg do
	case $arg in
		-h|--help)
	    	usage
		;;
	esac
done

# Check the other arguments
while [ $# -gt 1 ]
do
	key=$1
	case $key in
	    -p|--dir)
	    PATH_TO_PROJECT=$2
	    shift # past argument
	    ;;
	    -d|--dport)
	    DJANGO_PORT=$2
	    shift # past argument
	    ;;
	    -c|--mconf)
	    PATH_TO_MONGO_CONF=$2
	    shift # past argument
	    ;;
	    -m|--mport)
	    MONGO_PORT=$2
	    shift # past argument
	    ;;
	    -y|--py)
	    PYTHON=$2
	    shift # past argument
	    ;;
	    -l|--ce)
	    CELERY=$2
	    shift # past argument
	    ;;
	    -g|--mo)
	    MONGO=$2
	    shift # past argument
	    ;;
	esac
shift # past argument or value
done

if [[ -z $PATH_TO_PROJECT ]]; then
	  echo 'Path to django project folder is mandatory. Use --help if needed'
	  exit -1;
fi

if [[ -z $PATH_TO_MONGO_CONF ]]; then
	  echo 'Path to mongoDB configuration file is mandatory. Use --help if needed'
	  exit -1;
fi

# Check if server is already running
ERROR=false
PROC="$(pgrep mongod)"
if [[ -n $PROC ]]; then
	echo "Error: MongoDB is already running"
	ERROR=true
fi

PROC="$(pgrep celery)"
if [[ -n $PROC ]]; then
	echo "Error: Celery is already running"
	ERROR=true
fi

PROC="$(pgrep -f runserver)"
if [[ -n $PROC ]]; then
	echo "Error: Python server is already running"
	ERROR=true
fi

if [[ $ERROR = true ]]; then
	echo "You have to stop all running processes before launching the server."
	read -p "Would you like to kill all running processes ? (y or Y for yes) " -n 1 -r
	echo    # (optional) move to a new line
	if [[ ! $REPLY =~ ^[Yy]$ ]]; then
		echo "Terminated"
    		exit -1;
	fi
	echo "  --------------------Kill processes----------------------"
	pkill -f runserver
	pkill -f celery
	pkill -9 mongod

	echo "Resuming launch server..."
fi


# Launch server
cd $PATH_TO_PROJECT

echo "  ----------------------Start mongo-----------------------"
$MONGO --config $PATH_TO_MONGO_CONF --port $MONGO_PORT & disown
until nc -zv localhost $MONGO_PORT;
do
	sleep 1;
done

echo "  ---------------------Start celery-----------------------"
$CELERY -A $PROJ worker -l info -Ofair --purge & disown
until $CELERY -A $PROJ status;
do
	sleep 1;
done

echo "  ---------------------Start python-----------------------"
$PYTHON manage.py runserver --noreload 0.0.0.0:$DJANGO_PORT & disown
