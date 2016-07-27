@setlocal enableextensions
@cd /d "%~dp0"
@echo off

start cmd /k ..\mongodb\bin\mongod.exe --config ..\conf\mongodb.conf

echo Waiting for MongoDB to start...
timeout /t 5

start cmd /k "set PYTHONHOME=& ..\WinPython-32bit-2.7.6.3\python-2.7.6\python.exe ..\manage.py runserver"
echo Waiting for Server to run...
timeout /t 8

start http://127.0.0.1:8000