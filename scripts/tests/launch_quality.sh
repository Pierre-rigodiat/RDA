#!/bin/bash

pylint -f parseable admin_mdcs/ mgi/ api/ oai_pmh/ user_dashboard/ compose/ explore/ utils/ curate/ modules/ exporter/ utils/ testing/ | tee pylint.out