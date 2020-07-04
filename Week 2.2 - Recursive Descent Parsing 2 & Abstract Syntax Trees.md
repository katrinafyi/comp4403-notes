---
tags: [Notebooks/COMP4403]
title: Lecture 4 — Recursive Descent Parsing 2 & Abstract Syntax Trees
created: '2020-03-08T08:33:40.092Z'
modified: '2020-03-08T22:03:20.501Z'
---

# Lecture 4 &mdash; Recursive Descent Parsing 2 & Abstract Syntax Trees

We are continuing to take a grammar and write a Java parser for that grammar.

Refer to _RecursiveDescentParsing.pdf_ for examples of Java code for specific EBNF constructs.

Let's look at Terms now. $\textit{TERM} \to \textit{Factor }\{ \textit{ (TIMES | DIVIDE) Factor }\}$.
```java
int parseTerm() {
  int result;
  result = parseFactor();
  while (tokens.isIn(TERM_OPS_SET)) { // set of times and divide
    boolean times;
    if (tokens.isMatch(Token.TIMES)) {
      times = true;
      tokens.match(Token.TIMES);
    } else if (tokens.isMatch(Token.DIVIDE)) {
      times = false;
      tokens.match(Token.DIVIDE);
    } else {
      fatal("unknown term operator in set");
    }
    int factor = parseFactor();
    if (times) {
      result *= factor;
    } else {
      result /= factor;
    }
  }
  return result;
}
```

## Constructing an abstract syntax tree

Using the same example from above, we will parse a _Term_ into an AST. 

>_Term_ &rarr; _Factor_ { (_TIMES_ | _DIVIDE_) _Factor_ }.

```java
ExpNode parseTerm() {
  ExpNode result = parseFactor();
  while (tokens.isIn(TERM_OPS_SET)) { // set of times and divide
    Operator op = Operator.INVALID_OP;
    Location opLoc = tokens.getLocation();
    boolean times;
    if (tokens.isMatch(Token.TIMES)) {
      op = Operator.MUL_OP;
      tokens.match(Token.TIMES);
    } else if (tokens.isMatch(Token.DIVIDE)) {
      op = Operator.DIV_OP;
      tokens.match(Token.DIVIDE);
    } else {
      fatal("unknown term operator in set");
    }
    ExpNode factor = parseFactor();
    result = new ExpNode.BinaryNode(opLoc, op, result, factor);
  }
  return result;
}
```

Let's start with an expression `2 * 3 / 4`. Tracing the variables, with indentation roughly matching the code's indentation,
```java
result = ConstNode(l1, INTEGER_TYPE, 2); // r1
  // enter while loop, first
  op = INVALID_OP;
  opLoc = l2;
    op = MUL_OP;
  factor = ConstNode(l3, INTEGER_TYPE, 3); // f1
  result = BinaryNode(l2, MUL_OP, r1, f1); // r2
  // while loop, second
  op = INVALID_OP;
  opLoc = l4;
    op = DIV_OP;
  factor = ConstNode(l5, INTEGER_TYPE, 4); // f2
  result = BinaryNode(l4, DIV_OP, r2, f2);
return result;
```

## Syntax error recovery

_Moved to lecture 5._
