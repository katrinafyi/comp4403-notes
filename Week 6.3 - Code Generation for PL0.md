# Week 6.3 &mdash; Code Generation for PL0 Expressions and Statements

Consider a simple PL0 program:

```pascal
var x : int;
    y : int;
begin
  write 12 + 13
end
```

To generate the stack machine code, we have a new visitor CodeGenerator.java whose visit action is outputing the code for a particular node.

Special care is taken to handle different sizes of instructions and branches. See the statement visitors.