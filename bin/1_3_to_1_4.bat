@setlocal enableextensions
@cd /d "%~dp0"

start cmd /k "set PYTHONHOME=& ..\WinPython-32bit-2.7.6.3\python-2.7.6\python.exe ..\manage.py migrate"
start cmd /k "set PYTHONHOME=& ..\WinPython-32bit-2.7.6.3\python-2.7.6\python.exe ..\mgi\migrate.py -u admin -p admin"