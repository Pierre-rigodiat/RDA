#!/bin/bash
coverage run --source=mgi,api,oai_pmh,user_dashboard,compose ./manage.py test mgi/ api/ oai_pmh/ user_dashboard/ compose/ --liveserver=localhost:8082

