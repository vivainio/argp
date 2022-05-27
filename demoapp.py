import os
import time

import argp
argp.init()


def do_ls(args):
    if args.l:
        print("LONG format")

    print(os.listdir())


def do_pwd(args):

    print(os.getcwd())


def do_cls(args):
    if args.delay:
        print("Sleeping")
        time.sleep(args.delay)

    os.system("clear")

# this creates command with help:

"""
S C:\p\argp> python .\demoapp.py -h
usage: demoapp.py [-h] {files,other} ...

positional arguments:
  {files,other}
    files        Command group for handling files
    other        Other commands

optional arguments:
  -h, --help     show this help message and exit
PS C:\p\argp> python .\demoapp.py files -h
usage: demoapp.py files [-h] {ls,pwd} ...

positional arguments:
  {ls,pwd}
    ls        list files
    pwd       print working directory

optional arguments:
  -h, --help  show this help message and exit
  
PS C:\p\argp> python .\demoapp.py other -h
usage: demoapp.py other [-h] {cls} ...

positional arguments:
  {cls}
    cls       Clear screen

optional arguments:
  -h, --help  show this help message and exit  
"""


def main():
    fgroup = argp.group("files", help="Command group for handling files")
    lscmd = fgroup.sub("ls", do_ls, help="list files")
    lscmd.arg("-l", help="long format", action="store_true")
    fgroup.sub("pwd", do_pwd, help="print working directory")
    ogroup = argp.group("other", help="Other commands")
    cls = ogroup.sub("cls", do_cls, help="Clear screen")
    cls.arg("--delay", type=float, help="time to sleep before clearing")
    argp.parse()


if __name__ == "__main__":
    main()