"""No double files

A tool that filters duplicates out of a directory tree.
"""


import hashlib
import os
import re
import shutil
import string
import sys


OUTDIR = "output"
BLOCKSIZE = 104857600 # 100 MB


starterdir = os.path.dirname(os.path.realpath(__file__))


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


def calc_hash(filepath):
    """Build a hash sum of the content of the given file."""
    checksum = hashlib.sha256()
    with open(filepath, "rb") as f:
        while True:
            data = f.read(BLOCKSIZE)
            if not data:
                break
            checksum.update(data)
    return checksum.digest()


def filetree2filelist(root, subpath=""):
    """Get a list of all file paths under the given directory (first parameter).

    The paths in the returned list are relative to the given root path, meaning
    that they do not contain the given path. The second parameter "subpath" is
    for internal use only.
    """
    filelist = []

    for file in os.listdir(os.path.join(root, subpath)):
        filepath = os.path.join(subpath, file)
        if os.path.isdir(os.path.join(root, filepath)):
            filelist += filetree2filelist(root, filepath)
        else:
            filelist.append(filepath)

    getpathpartcount = lambda path: len(re.split(r"[/\\]", path))
    filelist.sort(key=getpathpartcount)

    return filelist


def copy(srcpath, dstpath):
    dstdir = os.path.split(dstpath)[0]
    os.makedirs(dstdir, exist_ok=True)
    shutil.copy2(srcpath, dstpath)


def parse_args(args):
    if len(args) != 2:
        error("Give directory.")
    src_dirpath = args[1]
    if not os.path.isdir(src_dirpath):
        error("Given argument is not a directory.")
    return src_dirpath


def main():
    src_dirpath = parse_args(sys.argv)

    dst_dirpath = os.path.join(starterdir, OUTDIR)
    if os.path.exists(dst_dirpath):
        shutil.rmtree(dst_dirpath)

    known_files = {}
    for file in filetree2filelist(src_dirpath):
        src_filepath = os.path.join(src_dirpath, file)
        dst_filepath = os.path.join(dst_dirpath, file)
        filehash = calc_hash(src_filepath)

        if filehash not in known_files.keys():
            log('Copy: "{}"'.format(src_filepath))
            copy(src_filepath, dst_filepath)
            known_files[filehash] = src_filepath
        else:
            log('Known: "{}" as "{}"'.format(src_filepath, known_files[filehash]))


if __name__ == "__main__":
    main()
