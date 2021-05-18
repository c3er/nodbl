param(
    [string]$DirPath
)

$tool = "$PSScriptRoot\nodbl.py"
$logFile = "$PSScriptRoot\copied.log"

& $tool $DirPath 2>&1 | Tee-Object $logFile
