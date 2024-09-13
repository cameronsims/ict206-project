REM Defines before we load the files
@ECHO off

REM Load python file
:RUN:
python "./src/main.py"

REM Repeat
echo Repeating Program...
pause
cls
goto RUN