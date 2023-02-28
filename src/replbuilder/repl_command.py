class ParserError(ValueError):
    pass


def parser_exit(*args):
    raise ParserError("argparse attempted to exit")


def parser_error(*args):
    print("\033[0;31merror parsing argument\033[0m")
    raise ParserError("argparse cannot parse argument")


def green_print(func):
    def print_wrapper(*args):
        print("\033[0;32m", end="")
        func(*args)
        print("\033[0m", end="")
    return print_wrapper


class ReplCommand:
    """Each instance represent one callable top level command

    Keyword arguments:
        - command: The name of the command, it should be a single string without special characters.
        - parser: argparse.ArgumentParser class, or object that support parse_args function. This
            parser will parse incoming command arguments, behaving as if it was passed in on shell
            level. Some ArgumentParser internals are overriden to make it work within a REPL.
        - runner: The function that will be invoked with the command, it would look like this:
                func(args)
                    - args would contain the parsed arguments
            If this function accept global context object from parent REPL execution:
                func(args, context)
                    - context would be passed in from ReplRunner.
            The function can also be in a class, were it would look like:
                func(self, args, context)
        - helpstr: A help string to describe what this command does.
        - use_context: If this is True, context will be passed in to the command from ReplRunner.
        - exception_handler: A custom exception handler (callable) to handle any exception.
    """

    def __init__(self, command, parser, runner, helpstr="", use_context=False, exception_handler=None):
        if any([not isinstance(command, str), " " in command]):
            raise ValueError("command must be a non-space delineated string")
        if not callable(getattr(parser, "parse_args", None)):
            raise ValueError("parser must support 'parse_args' function")
        if not callable(runner):
            raise ValueError("runner must be callable")
        if exception_handler and not callable(exception_handler):
            raise ValueError("exception handler must be callable")
        parser.exit = parser_exit # argparse use sysexit, override
        parser.error = parser_error
        parser.print_help = green_print(parser.print_help)
        parser.prog = command
        self.command = command # command string itself, e.g. "pip"
        self.parser = parser # argparse parser to parse the arguments
        self.runner = runner # runner that will be fed the parsed arguments
        self.helpstr = helpstr # help for overall command
        self.use_context = use_context # Use centralized context from ReplRunner
        self.exception_handler = exception_handler # Exception handler

    def run(self, command_input, context=None):
        """This function is invoked by ReplRunner whenever the command is invoked,
        It should not be invoked manually.

        This is not the implementation itself, but it attempt to:

            1. Parse the input of the command.
            2. If the input is help, display the help string for this particular command.
            3. Invoke the actual implementation (self.runner)
            4. Use custom exception_handler on potential exceptions if any is provided.
        """
        args = self.parser.parse_args(args=command_input)
        if command_input and command_input[0] in ["-h", "--help"]:
            return
        try:
            if self.use_context:
                self.runner(args, context)
            else:
                self.runner(args)
        except Exception as e:
            if self.exception_handler is None:
                raise e
            self.exception_handler(e)

