from replbuilder import ReplCommand, ReplRunner
import argparse


class Calculator:

    def add(self, args):
        print(args.x + args.y)

    def sub(self, args):
        print(args.x - args.y)

    def mult(self, args):
        print(args.x * args.y)

    def div(self, args):
        print(args.x / args.y)

    def pow(self, args):
        print(args.x ** args.y)

    def cowsay(self, args):
        word = args.word
        if not word:
            print("cowsay: moo")
        else:
            print("cowsay: {}".format(word))


def get_calc_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("x", type=float)
    parser.add_argument("y", type=float)
    return parser


def get_cowsay_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("-w", "--word", default=None, help="cow will say this")
    return parser


def main():
    calc_parser = get_calc_parser()
    cow_parser = get_cowsay_parser()
    calculator = Calculator()

    add_cmd = ReplCommand("add", calc_parser, calculator.add, "Add 2 numbers")
    sub_cmd = ReplCommand("sub", calc_parser, calculator.sub, "Subtract second number from first")
    mult_cmd = ReplCommand("mult", calc_parser, calculator.mult, "Multiply 2 numbers")
    div_cmd = ReplCommand("div", calc_parser, calculator.div, "Divide second number from first")
    pow_cmd = ReplCommand("pow", calc_parser, calculator.pow, "x to the power of y")
    cow_cmd = ReplCommand("cow", cow_parser, calculator.cowsay, "say stuff, demo optional")

    runner = ReplRunner("calculator")
    runner.add_commands([add_cmd, sub_cmd, mult_cmd, div_cmd, pow_cmd, cow_cmd])
    runner.run()


if __name__ == '__main__':
    main()
