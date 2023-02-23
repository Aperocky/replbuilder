## ReplBuilder

`pip install replbuilder`

Quickly build a repl cli prompt in python.

`argparse` is used for quick and easy parsing interface, some options are overriden for using it within a repl prompt. But you should be able to utilize the full power of `argparse` as your repl parser.

## Example

see [example calculator repl](example_calculator_repl.py) for example implementation. The gist can be concluded in a few lines:

```
add_cmd = ReplCommand("add", Calculator.basic_parser(), calculator.add, "Add 2 numbers")
sub_cmd = ReplCommand("sub", Calculator.basic_parser(), calculator.sub, "Subtract second number from first")
mult_cmd = ReplCommand("mult", Calculator.basic_parser(), calculator.mult, "Multiply 2 numbers")

# More advanced usage with exception handler and context obj:
fact_cmd = ReplCommand("factorial", Calculator.factorial_parser(), calculator.factorial, "factorial with exception handler", exception_handler=exception_handler)
say_cmd = ReplCommand("cowsay", Cow.get_cowsay_parser(), cow.cowsay, "say stuff, demo optional and context usage", use_context=True)
mood_cmd = ReplCommand("cowmood", argparse.ArgumentParser(), cow.cowmood, "Mood of the cow changes with global context object", use_context=True)

runner = ReplRunner("calculator", context)
runner.add_commands([add_cmd, sub_cmd, mult_cmd, fact_cmd, say_cmd, mood_cmd])
runner.run()
```

run it `python example_calculator_repl.py`

Part of the repl is colorized for better visibility:

![example repl run](demo.jpg)
