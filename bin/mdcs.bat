@setlocal enableextensions
@cd /d "%~dp0"

start cmd /k ..\mongodb\bin\mongod.exe --config ..\conf\mongodb.conf

while ! ..\mongo; do   
	timeout /t 1
done

start cmd /k "set PYTHONHOME=& ..\WinPython-32bit-2.7.6.3\python-2.7.6\python.exe ..\manage.py runserver"

timeout /t 8

start http://127.0.0.1:8000