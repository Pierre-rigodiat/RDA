#!/bin/bash


## declare an array variable
declare -a LIST_DIR_APP=()

usage()
{
	echo "  ---------------------------------------------------------------------"
	echo " | launch_tests_unix [DIR] [options]                                   |"
	echo " |                                                                     |"
	echo " |       Options:                                                      |"
	echo " |                                                                     |"
	echo " |  DIR           : paths to app folders to be tested                  |"
	echo " |  -h  | --help  : help                                               |"
	echo " |                                                                     |"
	echo "  ---------------------------------------------------------------------"
	exit -1;
}


# Check if there is no argument
if [[ -z $* ]]; then
	echo 'No argument found. All folders known to have tests will be tested. (mgi, api, user_dashboard, oai_pmh)'
	python manage.py test mgi/ user_dashboard/ oai_pmh/ api/ --liveserver=localhost:8082
	exit -1;
else
    for arg do
        case $arg in
            -h|--help)
                usage
            ;;
            *)
                if [ -d "$arg" ]; then
                    LIST_DIR_APP+=($arg)
                else
                    echo "Folder "$arg" doesn't exist"
                fi
            ;;
        esac
    done
fi

if [[ ${#LIST_DIR_APP[@]} -gt 0 ]]; then
    echo 'Arguments found. Starting to run the tests for: '${LIST_DIR_APP[@]}
    python manage.py test ${LIST_DIR_APP[@]} --liveserver=localhost:8082
else
    echo "No valid folders found. Terminated"
fi