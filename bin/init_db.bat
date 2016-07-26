@setlocal enableextensions
@cd /d "%~dp0"
@echo off


if exist "..\data\db" (
	echo ERROR: A database is already present
	pause
	exit
)

mkdir ..\data\db
start cmd /k ..\mongodb\bin\mongod.exe --config ..\conf\mongodb.conf

while ! ..\mongo; do   
	timeout /t 1
done

..\mongodb\bin\mongo.exe < create_admin.js

..\mongodb\bin\mongo.exe --port 27017 -u "admin" -p "admin" --authenticationDatabase admin < create_user.js

if not exist "..\db.sqlite3" (
	set PYTHONHOME=
	..\WinPython-32bit-2.7.6.3\python-2.7.6\python.exe ..\manage.py migrate
	..\WinPython-32bit-2.7.6.3\python-2.7.6\python.exe ..\manage.py createsuperuser
)

echo SUCCESS: Databases have been created with success.
pause