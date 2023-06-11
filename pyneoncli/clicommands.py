import argparse

from pyneoncli.neon import NeonObject
from pyneoncli.neonapi import NeonAPI
from pyneoncli.neonapiexceptions import NeonAPIException
from pyneoncli.printer import Printer
from pyneoncli.colortext import ColorText
from pyneoncli.msg import Msg


class CLICommands:

    def __init__(self, args: argparse.Namespace) -> None:
        self._args = args
        self._api_key = args.apikey
        self._api = NeonAPI(args.apikey)
        self._msg = Msg(no_color=args.nocolor)
        if args is None:
            self._p = Printer()
            self._c = ColorText()
        else:
            self._p = Printer(nocolor=args.nocolor, filters=args.fieldfilter)
            self._c = ColorText(no_color=args.nocolor)

    @property
    def args(self):
        return self._args

    @args.setter
    def args(self, value):
        self._args = value
        self._p = Printer(nocolor=self._args.nocolor, filters=self._args.fieldfilter)
        self._c = ColorText(no_color=self._args.nocolor)

    def print_obj_id(self, label, p:NeonObject, indent=0, sep=": ", end="\n"):
        indent = " " * indent
        name_str = None
        id_str = None

        if not isinstance(p, NeonObject):
            raise NeonAPIException("Object is not a NeonObject at print_obj_id")

        if "id" in p.obj_data:
            id_str = p.id
        if "name" in p.obj_data:
            name_str = p.name

        if name_str is None and id_str is None:
            raise NeonAPIException("No name or id found in object at print_object-Id")
        elif name_str is None:
            self._msg.kv(f"{indent}{label}", f"{self._c.yellow(id_str)}", sep=sep, end=end)
        else:
            self._msg.kv(f"{indent}{label}", f"{name_str}:{self._c.yellow(id_str)}", sep=sep, end=end)

    def report_exception(self, e:NeonAPIException, op: str, msg: str):
        self._msg.error_kv(op, msg)
        self._msg.error_kv("  Status Code", e.err.response.status_code)
        self._msg.error_kv("  Reason", e.err.response.reason)
        self._msg.error_kv("  Text", e.err.response.text)


