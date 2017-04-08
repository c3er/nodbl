@echo off

set TOOL="%~dp0nodbl.py"
set LOGFILE="%~dp0copied.log"
set ERRORFILE="%~dp0%errors.log"

%TOOL% %1 > %LOGFILE% 2> %ERRORFILE%

if ERRORLEVEL 1 goto FAIL
goto EXITPOINT

:FAIL
type %ERRORFILE%

:EXITPOINT
pause
