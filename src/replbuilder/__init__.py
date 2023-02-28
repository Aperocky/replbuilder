"""
ReplBuilder
-----------

Quickly build your custom commands into a custom repl.

Use replbuilder.ReplCommand class to build any custom command.
Use replbuilder.ReplRunner to orchestrate and run those commands.

Fully colorized, perfect for building operation tools and other client specific command line interface. This allows a simple CLI to keep context between different command execution, simplifying how it should run:

    add_cmd = ReplCommand("add", basic_parser, calculator.add, "Add 2 numbers")
    sub_cmd = ReplCommand("sub", basic_parser, calculator.sub, "Subtract second number from first")
    fact_cmd = ReplCommand("factorial", factorial_parser, calculator.factorial, "factorial with exception handler", exception_handler=exception_handler)
    runner = ReplRunner("calculator")
    runner.add_commands([add_cmd, sub_cmd, fact_cmd], namespace="Calculator") # namespace is optional
    runner.run() # You're running a repl with 3 calculator commands!

The commands are built with argparse, this makes helpstring useful and straightforward to achieve.
"""
from .repl_command import ReplCommand
from .repl_runner import ReplRunner
