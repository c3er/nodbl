# No double files

A tool that filters doubled files out of a directory tree.

## Requirements

Python 3.5 or newer is needed to run the tool.

The tool, all batch files and the PowerShell script are tested under Windows 10 only.

## Usage

The tool copies the given directory to a new "output" directory without the files that are definitely doubled. This is determined by calculating checksums of their content.

### Call tool directly

This example assumes that you opened a PowerShell in the directory of the tool:

```
.\nodbl.py path\to\directory\of\interest\
```

### Other files

There are some batch files that make it more comfortable to use te tool. It is recommended to use `nodbl.cmd` that calls the PowerShell script `nodbl.ps1`. It is possible to drag&drop the directory of interest to these batch files. As usual the output directory will be in the same place as the tool (and the batch files).

#### `nodbl.cmd`

Prints which files are copied or already known and errors to the console and to the log file `copied.log`.

#### `nodbl-interactive.cmd`

Prints which files are copied or already known and errors to the console only.

#### `nodbl-log.cmd`

Prints which files are copied or already known to the log file `copied.log` only. Errors are printed to the log file `errors.log` and to the console.