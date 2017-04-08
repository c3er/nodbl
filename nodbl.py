#!/usr/bin/env python
# -*- coding: utf-8 -*-


import sys
import os
import re
import string
import hashlib
import shutil


OUTDIR = "output"
BLOCKSIZE = 104857600  # 100 MB


def error(msg):
    print(msg, file=sys.stderr)
    exit(1)


def getscriptpath(script):
    return os.path.dirname(os.path.realpath(script))


def gethash(filepath):
    checksum = hashlib.md5()
    with open(filepath, "rb") as f:
        while True:
            data = f.read(BLOCKSIZE)
            if not data:
                break
            checksum.update(data)
    return checksum.digest()


def getfilelist(root, subpath=""):
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


def str2ascii(text):
    charlist = list(text)
    for i, char in enumerate(charlist):
        if char not in string.printable:
            charlist[i] = "&#" + str(ord(char)) + ";"
    return "".join(charlist)


def main():
    args = sys.argv
    if len(args) != 2:
        error("Give directory.")

    dirpath = args[1]
    if not os.path.isdir(dirpath):
        error("Given argument is not a directory.")

    outdir = os.path.join(getscriptpath(__file__), OUTDIR)
    known_files = {}
    for file in getfilelist(dirpath):
        srcpath = os.path.join(dirpath, file)
        dstpath = os.path.join(outdir, file)
        filehash = gethash(srcpath)
        
        if filehash not in known_files.keys():
            print(str2ascii('Copy: "{}"'.format(srcpath)))
            copy(srcpath, dstpath)
            known_files[filehash] = srcpath
        else:
            print(str2ascii('Known: "{}" as "{}"'.format(srcpath, known_files[filehash])))


if __name__ == "__main__":
    main()
