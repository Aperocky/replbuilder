### 1.0.5

Minor bugfix: Prevent registering of reserved keywords (e.g. `help`, `exit`) as commands.

### 1.0.4

Minor update: When help strings are long and requires wrapping when listing, do not wrap them under the commands, and tuck the description block nicely to the side.

### 1.0.3

Minor update: `ls` to work the same way as `help` in displaying all available commands.

### 1.0.2

Minor bugfix: Gracefully handle keyboard interrupt.

### 1.0.1

Minor update: Added a blank line after each command output for aesthetic and visibility.

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
