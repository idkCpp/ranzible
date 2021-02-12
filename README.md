
# ranzible

Introducing `ranzible`, an alternative syntax for calling ansible modules.

# How it works

Instead of writing playbooks in YAML with folder structures that store various information across files you can write playbooks using the ranzible language.

Ranzible is closly based on the ansible YAML structure.
There are plays and roles and host vars and group vars.
But then there is more.

In ansible working with default vars and overriding these in role dependencies can be cumbersome.
Ranzible provides an easy C+YAML-inspired syntax for managing roles and calling modules.

## Foundation principles

Less magic, more verbose code.

The ranzible syntax is quite verbose.
But this is intended.

A ranzible document can have the following definitions:
* Play Definitons
* Role Definitons

Plays and roles can have variables.
Variables have a scope that has to be defined in its defining line.
The following scopes are supported:
* `host` - the variable is stored in the current host
* `role` - the variable is available in the current role's body, every host has it's own copy
* `block` - the variable is available in the current block's body, every host has it's own copy

To obtain the value of another host's variable use the `peek` command.
To update the value of another host's variable use the `push` command.

Since ranzible is, just like ansible, written in python, there are the following variable types:
* String
* Integer
* Float
* Bool
* None
* List
* Object

Any variables are always passed by value.
The callee can never alter variables of the caller, also there are no return values.

## Defining plays

TODO

## Defining roles

Role definitions can be specified in any ranzible document.

Let's see this example, that just executes a shell command on the remote host via ansibles `shell` module.

```
role hostname () {
	variable role command_to_execute: 'hostname';

	"Execute the command" module shell(cmd: command_to_execute);
}
```

This is a very simple example, but it illustrates how to define a role, a variable and how to invoke an ansible module.

This role takes no parameters.
It defines a variable that is only available within this role.
It calls the ansible module `shell` with the parameter `cmd` set to the previously defined variable.
The module call is prepended with a name string. This is equivalent to specifying `name` in ansibles YAML-syntax.

