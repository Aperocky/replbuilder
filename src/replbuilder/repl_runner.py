import argparse
import os
import re
import textwrap
import sys
import shlex
import readline
from .repl_command import ReplCommand, ParserError
from collections import namedtuple


CmdHelp = namedtuple("CmdHelp", "cmd help")


class ReplRunner:
    """The orchestrator and runner of the REPL.

    Keyword Arguments
        - name: [optional] [default="repl"]
            Name of the repl, it will be displayed before each command is entered, e.g.:
            YourReplName > command --arg_name arg_val
        - context: [optional]
            A context object, this can be potentially passed to all commands that are marked
            use_context=True. this is very useful as state, common objects, and data can be
            stored in the context object.
        - catch_exception: [optional] [default=True]
            Catch any exception thrown from any commands and show their message, this blocks
            exceptions from interrupting the main REPL and exiting the CLI environment. However,
            it maybe useful to turn it off for debug purposes.
        - vi_mode: [optional] [default=False]
            Use vi mode within the CLI environment, highly recommend if you use vim
    """

    def __init__(self, name="repl", context=None, catch_exception=True, vi_mode=False):
        self.name = name
        self.commands = {} # {string: ReplCommand} dict, this is where commands are stored.
        self.context = context # Context object, orchestrator will pass it to commands if specified
        self.command_namespaces = {"Default": [], "Alias": []} # Namespaces for helpstr organization
        self.catch_exception = catch_exception
        self.aliases = {}
        if vi_mode:
            readline.parse_and_bind("set editing-mode vi")

    def add_commands(self, repl_commands, namespace=None):
        """Add commands to the cli orchestrator

        Keyword Arguments:
            - repl_commands: a list of ReplCommands
            - namespace: [optional]
                A string to indicate the namespace the command belong to for organization
        """
        if self.aliases:
            raise ValueError("Command should be added before aliases are populated")
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

    def add_aliases(self, aliases):
        """Add aliases to the cli orchestrator

        aliases are translated as is, this allow shortening of some commands and
        embedding of common arguments.

        Keyword Arguments
            - aliases: a dictionary of {alias: translation} pairs
        """
        if any(s in aliases for s in ReplCommand.RESERVED_STRINGS):
            raise ValueError("Aliases must not conflict with existing strings")
        if any(s in aliases for s in self.commands):
            raise ValueError("Aliases must not conflict with existing commands")
        if any(not re.match(r"^\w+$", s) for s in aliases.keys()):
            raise ValueError("Aliases must be a single contiguous string")
        self.aliases.update(aliases)
        chs = [CmdHelp(k, v) for k, v in aliases.items()]
        self.command_namespaces["Alias"].extend(chs)

    def run(self):
        """This invokes the repl cli environment

        Register commands and aliases before invoking this.
        """
        while True:
            try:
                cmd_input = input("\033[0;33m{} > \033[0m".format(self.name))
                self.run_command(cmd_input)
            except KeyboardInterrupt as e:
                print("Leaving {}".format(self.name))
                return
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
        if command in ["help", "h", "ls"]:
            self.help()
            return
        if command in ["exit", "q", "exit()"]:
            print("Leaving {}".format(self.name))
            sys.exit(0)
        if command in self.aliases:
            # Translate aliases into full commands
            alias_trans = self.aliases[command]
            new_cmd = " ".join([alias_trans] + cmd_split[1:])
            self.run_command(new_cmd)
            return
        if command in self.commands:
            self.commands[command].run(cmd_split[1:], self.context)
            print() # Add a space after output and prior to next input for clear delineation.
            sys.stdout.flush() # Flush buffer to prevent pollution.
        else:
            print("\033[0;31mCommand {} not found\033[0m".format(command))

    def print_cmd_help(self, ch, maxlen, default=False, alias=False):
        term_width = os.get_terminal_size().columns
        line_width = term_width - maxlen - 24
        helplines = textwrap.wrap(ch.help, line_width)
        if not helplines:
            helplines.append("")
        if default:
            print("\033[0;36m{command: <{pad}}\033[0m{desc}"
                .format(command=ch.cmd, pad=maxlen+8, desc=helplines[0]))
        elif alias:
            print("\033[3;37m    {command: <{pad}}\033[0;37m{desc}\033[0m"
                .format(command=ch.cmd, pad=maxlen+4, desc=helplines[0]))
        else:
            print("\033[0;36m    {command: <{pad}}\033[0m{desc}"
                .format(command=ch.cmd, pad=maxlen+4, desc=helplines[0]))
        for line in helplines[1:]:
            print(" "*(maxlen + 8) + line)

    def help(self):
        """This provides the global help string of all commands, separated by namespace,
        if namespaces are given.
        """
        print("\033[0;32mList of available commands:")
        maxlen = max(map(lambda c: len(c), self.commands))
        default_commands = self.command_namespaces["Default"]
        if default_commands:
            for c in default_commands:
                self.print_cmd_help(c, maxlen, default=True)
        # custom namespaces in their own sections
        for namespace, clist in self.command_namespaces.items():
            if namespace in ["Default", "Alias"]:
                continue
            print("\033[1;35m{}\033[0m".format(namespace))
            for c in clist:
                self.print_cmd_help(c, maxlen)
        if self.command_namespaces["Alias"]:
            print("\033[3;35m{}\033[0m".format("Alias"))
            for c in self.command_namespaces["Alias"]:
                self.print_cmd_help(c, maxlen, alias=True)

