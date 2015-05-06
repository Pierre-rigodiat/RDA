@setlocal enableextensions
@cd /d "%~dp0"
start cmd /k ..\mongodb\bin\mongod.exe --conf ..\conf\mongodb.conf
start cmd /k ..\jre7\bin\java.exe -jar ..\rdf\JenaServers.jar -rdfserver_endpoint "tcp://127.0.0.1:5555" -sparqlserver_endpoint "tcp://127.0.0.1:5556" -tdb_directory ..\data\ts -project_uri "http://www.example.com"
start cmd /k ..\WinPython-32bit-2.7.6.3\python-2.7.6\python.exe ..\manage.py runserver


