#CQRS - Command Quary Responsibility Segregation

CQRS, which means Command Query Responsibility Segregation, comes from CQS (Command Query Separation) introduced by Bertrand Meyer in Object Oriented Software Construction. Meyer states that every method should be either a query or a command.

The difference between CQS and CQRS is that every CQRS object is divided in two objects: one for the query and one for the command.

A command is defined as a method that changes state. On the contrary, a query only returns a value.

The following schema shows a basic implementation of the CQRS pattern inside an application. All messages are sent through commands and events. Let’s take a closer look at this.

Read more [here](https://medium.com/eleven-labs/cqrs-pattern-c1d6f8517314)

## Why CQRS fits blockchain model
