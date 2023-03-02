import argparse
import sys
import shlex
import readline
from .repl_command import ReplCommand, ParserError
from collections import namedtuple


CmdHelp = namedtuple("CmdHelp", "cmd help")


class ReplRunner:
    """The orchestrator and runner of the REPL.

    Keyword Arguments
        - name: Name of the repl, it will be displayed before each command is entered, e.g.:
            YourReplName > command --arg_name arg_val
        - context:
            A context object, this can be potentially passed to all commands that are marked
            use_context=True. this is very useful as state, common objects, and data can be
            stored in the context object.
        - catch_exception:
            Catch any exception thrown from any commands and show their message, this blocks
            exceptions from interrupting the main REPL and exiting the CLI environment. However,
            it maybe useful to turn it off for debug purposes.
    """

    def __init__(self, name="repl", context=None, catch_exception=True):
        self.name = name
        self.commands = {}
        self.context = context
        # Group commands via namespace for display
        self.command_namespaces = {"Default": []}
        self.catch_exception = catch_exception

    def add_commands(self, repl_commands, namespace=None):
        """Add commands to the REPL

        This take a list of ReplCommands and register them with ReplRunner

        It can also take namespace argument, with which provided commands will
        be listed under that namespace together, for better organization and
        visibility.
        """
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
        """This invokes the REPL with all registered commands."""
        while True:
            try:
                cmd_input = input("\033[0;33m{} > \033[0m".format(self.name))
                self.run_command(cmd_input)
            except ParserError as e:
                pass
            except Exception as e:
                if self.catch_exception:
                    print("\033[0;31mCaught {}: {}\033[0m".format(type(e).__name__, e))
                else:
                    raise e

    def run_command(self, cmd_input):
        """Whenever return key is pressed in the REPL, it will invoke this function.

        This function does a little sanity check to make sure the command make sense:

            1. If it's an empty string, don't do anything.
            2. If it is "help", show the global help string of all commands.
            3. If it is "exit", end the program.
            4. If the command is within the list of command registered, invoke that.
        """
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
            print() # Add a space after output and prior to next input for clear delineation.
        else:
            print("\033[0;31mCommand {} not found\033[0m".format(command))

    def help(self):
        """This provides the global help string of all commands, separated by namespace,
        if namespaces are given.
        """
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
