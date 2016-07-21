#!/bin/bash
pkill -f runserver
pkill -f celery
pkill -9 mongod