from replbuilder import ReplCommand, ReplRunner
import argparse
import random


class Calculator:

    @staticmethod
    def basic_parser():
        parser = argparse.ArgumentParser()
        parser.add_argument("x", type=float, help="a number")
        parser.add_argument("y", type=float, help="another number")
        return parser

    @staticmethod
    def factorial_parser():
        parser = argparse.ArgumentParser()
        parser.add_argument("x", type=int, help="must be integer no larger than 100")
        return parser

    def add(self, args):
        print(args.x + args.y)

    def sub(self, args):
        print(args.x - args.y)

    def mult(self, args):
        print(args.x * args.y)

    def factorial(self, args):
        x = args.x
        if x > 100:
            raise ValueError("Too large for factorial")
        result = 1
        while x > 1:
            result *= x
            x -= 1
        print(result)


class Cow:

    @staticmethod
    def get_cowsay_parser():
        parser = argparse.ArgumentParser()
        parser.add_argument("-w", "--word", default=None, help="cow will say this")
        return parser

    def cowsay(self, args, context):
        word = args.word
        if not word:
            print("cowsay: {}".format(context.word))
        else:
            print("cowsay: {}".format(word))

    def cowmood(self, args, context):
        print("cow feels {}".format(context.mood))
        context.generate_random_mood()


class CowContext:

    # In real world, this context here would entail clients/state or data
    # To be populated, modified, used or passed between commands.
    def __init__(self):
        self.word = "replbuilder is a fast and easy way to build repl cli"
        self.mood = "MOO"

    def generate_random_mood(self):
        self.mood = ["MOO", "MOOMOO", "MUMUMU", "UNC"][random.randint(0, 3)]


def exception_handler(e):
    print("custom exception_handler caught {}: {}".format(type(e).__name__, e))


def main():
    calculator = Calculator()
    cow = Cow()
    cow_context = CowContext()
    commands = []

    # Calculator commands
    add_cmd = ReplCommand("add", Calculator.basic_parser(), calculator.add, "Add 2 numbers")
    sub_cmd = ReplCommand("sub", Calculator.basic_parser(), calculator.sub, "Subtract second number from first")
    mult_cmd = ReplCommand("mult", Calculator.basic_parser(), calculator.mult, "Multiply 2 numbers")
    fact_cmd = ReplCommand("factorial", Calculator.factorial_parser(), calculator.factorial, "factorial with exception handler", exception_handler=exception_handler)
    commands.extend([add_cmd, sub_cmd, mult_cmd, fact_cmd])

    # Cow commands
    say_cmd = ReplCommand("cowsay", Cow.get_cowsay_parser(), cow.cowsay, "say stuff, demo optional and context usage", use_context=True)
    mood_cmd = ReplCommand("cowmood", argparse.ArgumentParser(), cow.cowmood, "Mood of the cow changes with global context object", use_context=True)
    commands.extend([say_cmd, mood_cmd])

    # Running repl with above commands
    runner = ReplRunner("cowculator", cow_context)
    runner.add_commands(commands)
    runner.run()


if __name__ == '__main__':
    main()
