#!/usr/bin/env python
# -*- coding: utf-8 -*-


"""No double files

A tool that filters doubled files out of a directory tree.
"""


import sys
import os
import re
import string
import hashlib
import shutil


OUTDIR = "output"
BLOCKSIZE = 104857600  # 100 MB


def str2ascii(text):
    charlist = list(text)
    for i, char in enumerate(charlist):
        if char not in string.printable:
            charlist[i] = "&#" + str(ord(char)) + ";"
    return "".join(charlist)


def log(*args, sep=" ", **kw):
    """Helper to ensure that messages are flushed to stdout directly."""
    print(str2ascii(sep.join(args)), **kw, flush=True)


def error(msg):
    log(msg, file=sys.stderr)
    exit(1)


def getscriptpath(script):
    return os.path.dirname(os.path.realpath(script))


def gethash(filepath):
    """Build a hash sum of the content of the given file."""
    checksum = hashlib.sha256()
    with open(filepath, "rb") as f:
        while True:
            data = f.read(BLOCKSIZE)
            if not data:
                break
            checksum.update(data)
    return checksum.digest()


def getfilelist(root, subpath=""):
    """Get a list of all file paths under the given directory (first parameter).

    The paths in the returned list are relative to the given root path, meaning
    that they do not contain the given path. The second parameter "subpath" is
    for internal use only.
    """
    filelist = []

    for file in os.listdir(os.path.join(root, subpath)):
        filepath = os.path.join(subpath, file)
        if os.path.isdir(os.path.join(root, filepath)):
            filelist += getfilelist(root, filepath)
        else:
            filelist.append(filepath)

    getpathpartcount = lambda path: len(re.split(r"[/\\]", path))
    filelist.sort(key=getpathpartcount)

    return filelist


def copy(srcpath, dstpath):
    dstdir = os.path.split(dstpath)[0]
    os.makedirs(dstdir, exist_ok=True)
    shutil.copy(srcpath, dstpath)


def main():
    args = sys.argv
    if len(args) != 2:
        error("Give directory.")

    dirpath = args[1]
    if not os.path.isdir(dirpath):
        error("Given argument is not a directory.")

    outdir = os.path.join(getscriptpath(__file__), OUTDIR)
    if os.path.exists(outdir):
        shutil.rmtree(outdir)

    known_files = {}
    for file in getfilelist(dirpath):
        srcpath = os.path.join(dirpath, file)
        dstpath = os.path.join(outdir, file)
        filehash = gethash(srcpath)
        
        if filehash not in known_files.keys():
            log('Copy: "{}"'.format(srcpath))
            copy(srcpath, dstpath)
            known_files[filehash] = srcpath
        else:
            log('Known: "{}" as "{}"'.format(srcpath, known_files[filehash]))


if __name__ == "__main__":
    main()
