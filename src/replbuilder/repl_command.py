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

