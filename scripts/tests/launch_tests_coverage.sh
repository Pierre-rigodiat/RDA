#!/bin/bash
coverage run --source=mgi,api,oai_pmh,user_dashboard ./manage.py test mgi/ api/ oai_pmh/ user_dashboard/ --liveserver=localhost:8082

