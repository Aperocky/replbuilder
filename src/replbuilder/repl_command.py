class ParserError(ValueError):
    pass


def parser_exit(*args):
    raise ParserError("argparse attempted to exit")


def parser_error(func):
    print("\033[0;31merror parsing argument\033[0m")
    raise ParserError("argparse cannot parse argument")


def green_print(func):
    def print_wrapper(*args):
        print("\033[0;32m", end="")
        func(*args)
        print("\033[0m", end="")
    return print_wrapper


class ReplCommand:

    def __init__(self, command, parser, runner, helpstr=""):
        if any([not isinstance(command, str), " " in command]):
            raise ValueError("command must be a non-space delineated string")
        if not callable(getattr(parser, "parse_args", None)):
            raise ValueError("parser must support 'parse_known_args' function")
        if not callable(runner):
            raise ValueError("runner must be callable")
        parser.exit = parser_exit
        parser.error = parser_error
        parser.print_help = green_print(parser.print_help)
        parser.prog = command
        self.command = command # command string itself, i.e. "pip"
        self.parser = parser # argparse parser to parse the arguments
        self.runner = runner # runner that will be fed the parsed arguments
        self.helpstr = helpstr

    def run(self, command_input):
        args = self.parser.parse_args(args=command_input)
        if command_input and command_input[0] in ["-h", "--help"]:
            return
        self.runner(args)

