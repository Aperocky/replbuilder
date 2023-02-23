import argparse
import sys
import shlex
import readline
from .repl_command import ReplCommand, ParserError


class ReplRunner:

    def __init__(self, name="repl", context=None):
        self.name = name
        self.commands = {}
        self.context = context

    def add_commands(self, repl_commands):
        for repl_cmd in repl_commands:
            if not isinstance(repl_cmd, ReplCommand):
                raise ValueError("Commands added must be ReplCommand type")
            self.commands[repl_cmd.command] = repl_cmd

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
        print("\033[0;32m", end="")
        print("List of available commands: ")
        longest = max(map(lambda c: len(c), self.commands))
        for name, cmd in self.commands.items():
            print("\033[0;36m{command: <{pad}}\033[0m{desc}".format(command=name, pad=longest+8, desc=cmd.helpstr))
