@echo off

"%~dp0nodbl.py" %1 > "%~dp0copied.log" 2> "%~dp0errors.log"
pause