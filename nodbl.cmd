@echo off
:: Based on: https://www.howtogeek.com/204088/how-to-use-a-batch-file-to-make-powershell-scripts-easier-to-run/

PowerShell.exe -Command "& '%~dpn0.ps1'" "'%1'"
pause
