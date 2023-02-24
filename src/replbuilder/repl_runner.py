import argparse
import sys
import shlex
import readline
from .repl_command import ReplCommand, ParserError
from collections import namedtuple


CmdHelp = namedtuple("CmdHelp", "cmd help")


class ReplRunner:

    def __init__(self, name="repl", context=None):
        self.name = name
        self.commands = {}
        self.context = context
        # Group commands via namespace for display
        self.command_namespaces = {"Default": []}

    def add_commands(self, repl_commands, namespace=None):
        chs = []
        for repl_cmd in repl_commands:
            if not isinstance(repl_cmd, ReplCommand):
                raise ValueError("Commands added must be ReplCommand type")
            self.commands[repl_cmd.command] = repl_cmd
            chs.append(CmdHelp(repl_cmd.command, repl_cmd.helpstr))
        if namespace is None:
            self.command_namespaces["Default"].extend(chs)
        else:
            if namespace in self.command_namespaces:
                self.command_namespaces[namespace].extend(chs)
            else:
                self.command_namespaces[namespace] = chs

    def run(self):
        while True:
            try:
                cmd_input = input("\033[0;33m{} > \033[0m".format(self.name))
                self.run_command(cmd_input)
            except ParserError as e:
                pass
            except InterruptedError:
                raise

    def run_command(self, cmd_input):
        cmd_split = shlex.split(cmd_input)
        if not cmd_split:
            return
        command = cmd_split[0]
        if command in ["help", "h"]:
            self.help()
            return
        if command in ["exit", "q", "exit()"]:
            print("Leaving {}".format(self.name))
            sys.exit(0)
        if command in self.commands:
            self.commands[command].run(cmd_split[1:], self.context)
        else:
            print("\033[0;31mCommand {} not found\033[0m".format(command))

    def help(self):
        print("\033[0;32mList of available commands:")
        maxlen = max(map(lambda c: len(c), self.commands))
        default_commands = self.command_namespaces["Default"]
        if default_commands:
            for c in default_commands:
                print("\033[0;36m{command: <{pad}}\033[0m{desc}"
                .format(command=c.cmd, pad=maxlen+8, desc=c.help))
        # custom namespaces in their own sections
        for namespace, clist in self.command_namespaces.items():
            if namespace == "Default":
                continue
            print("\033[0;35m{}\033[0m".format(namespace))
            for c in clist:
                print("\033[0;36m    {command: <{pad}}\033[0m{desc}"
                .format(command=c.cmd, pad=maxlen+4, desc=c.help))
