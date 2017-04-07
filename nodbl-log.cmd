@echo off

set ERRORFILE="%~dp0%errors.log"

"%~dp0nodbl.py" %1 > "%~dp0copied.log" 2> %ERRORFILE%

if ERRORLEVEL 1 goto FAIL
goto EXITPOINT

:FAIL
echo Unexpected error occured:
type %ERRORFILE%

:EXITPOINT
pause
