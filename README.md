## ReplBuilder

`pip install replbuilder`

Quickly build a repl cli prompt in python.

`argparse` is used for quick and easy parsing interface, some options are overriden for using it within a repl prompt. But you should be able to utilize the full power of `argparse` as your repl parser.

## Example

see [example calculator repl](example_calculator_repl.py) for example implementation. The gist can be concluded in a few lines:

```
add_cmd = ReplCommand("add", calc_parser, calculator.add, "Add 2 numbers")
sub_cmd = ReplCommand("sub", calc_parser, calculator.sub, "Subtract second number from first")
mult_cmd = ReplCommand("mult", calc_parser, calculator.mult, "Multiply 2 numbers")
...

runner = ReplRunner("calculator")
runner.add_commands([add_cmd, sub_cmd, mult_cmd, div_cmd, pow_cmd, cow_cmd])
runner.run()
```

run it `python example_calculator_repl.py`

Part of the repl is colorized for better visibility:

![example repl run](demo.jpg)
