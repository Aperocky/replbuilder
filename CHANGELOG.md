### 1.2.1

Adding test to its own file.

### 1.2.0

Fixes linewrap issues, this does impact coloring, but now lines wrap correctly.

### 1.1.1

Add flush after each command

### 1.1.0

feature release: add `add_aliases` to allow `alias` mapping for longer command and arguments. 

Note: some previously accepted commands (e.g. "my-command") may stop working as this new version enforces regex `^\w+$` for command string, `_` would still work. This is a good restriction in my opinion to avoid confusion on the argument parser.

### 1.0.6

small update: add `vi_mode` flag to runner to allow cli env key binding in `vi` mode.

### 1.0.5

bugfix: Prevent registering of reserved keywords (e.g. `help`, `exit`) as commands.

### 1.0.4

bugfix: When help strings are long and requires wrapping when listing, do not wrap them under the commands, and tuck the description block nicely to the side.

### 1.0.3

small update: `ls` to work the same way as `help` in displaying all available commands.

### 1.0.2

bugfix: Gracefully handle keyboard interrupt.

### 1.0.1

small update: Added a blank line after each command output for aesthetic and visibility.

### 1.0.0

It is ready! Added docstrings for classes.

### 0.5.0

Catch command exceptions globally, optional opt out. Custom exception handler can be used to override global exception handling.

### 0.4.0

Allow grouping of commands into namespaces, add testing heredoc.

### 0.3.0

Allow a central, user defined context object to be passed into commands from runner for persistence of state, injection and other uses.

Allow custom exception handler to be passed into each command.

### 0.2.0

Use `readlines` for better cli env.

### 0.1.0

Initial commit
