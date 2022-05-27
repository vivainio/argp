""" Quick and dirty wrapper for argparse, with the intent to be less verbose

Meant to be used like this::

    import argp
    s1 = argp.sub("check", do_check)
    s2 = argp.sub("sign", do_sign, help="Sign the delivery")

    s2.arg("signature", metavar="SIGNATURE")

    argp.parse()
"""

import argparse, sys

# yes, 'p' will contain the parser
from typing import Callable, Any

p: argparse.ArgumentParser
subparsers: Any = None


def init(parser: argparse.ArgumentParser = None) -> argparse.ArgumentParser:
    """This module needs to be initialized by 'init'.

    Can be called with parser to use a pre-built parser, otherwise
    a simple default parser is created
    """

    global p, subparsers
    if parser is None:
        p = argparse.ArgumentParser()
    else:
        p = parser

    subparsers = p.add_subparsers(required=True, dest="command")

    return p


def parse_list(l: list) -> argparse.Namespace:
    """ call if you want to provide the list yourself, instead of defaulting to sys.argv[1:] (as with parse) """
    parsed = p.parse_args(l)
    dispatch_parsed(parsed)
    return parsed


def dispatch_parsed(parse_result: argparse.Namespace):
    """ Call this if you did 'ArgumentParser.parse_arguments' yourself """
    if "func" in parse_result:
        parse_result.func(parse_result)


def parse_or_show_help():
    """ Show -h usage message if called without arguments """
    argv = sys.argv[1:]
    if not argv:
        argv = ["-h"]
    parse_list(argv)


def parse():
    """Call this after declaring your arguments"""
    parse_list(sys.argv[1:])


def sub(name: str, func: Callable, **kwarg) -> argparse.ArgumentParser:
    """Add subparser to top level parser"""
    sp = subparsers.add_parser(name, **kwarg)
    _patch_subparser(sp)

    sp.set_defaults(func=func)
    return sp


def _patch_subparser(sp: argparse.ArgumentParser):
    sp.arg = sp.add_argument


def group(name: str, **kwargs) -> argparse.ArgumentParser:
    """ add group (for hierarchy)

    """

    global subparsers
    sp = subparsers.add_parser(name, **kwargs)
    _patch_subparser(sp)
    own_subparsers = sp.add_subparsers(required=True, dest="command")

    def do_sub(sname: str, func: Callable, **kwargs):
        parser = own_subparsers.add_parser(sname, **kwargs)
        _patch_subparser(parser)
        parser.set_defaults(func=func)
        return parser

    sp.sub = do_sub
    return sp
