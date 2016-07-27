#!/bin/bash
coverage run --source=mgi,api,oai_pmh,user_dashboard,compose,explore ./manage.py test mgi/ api/ oai_pmh/ user_dashboard/ compose/ explore/ --liveserver=localhost:8082 --no-selenium

