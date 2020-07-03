---
tags: [Notebooks/COMP4403]
title: Lecture 5 — Syntax Error Recovery
created: '2020-03-08T22:02:58.009Z'
modified: '2020-03-10T02:42:56.743Z'
---

# Lecture 5 &mdash; Syntax Error Recovery

Remark: For this parsing method, the first symbols of any alternative must be pairwise disjoint.

There are a few parts to syntax error recovery, such as when parsing and when matching. For example, when a syntax error is encountered it can throw away unexpected tokens or replace tokens with the correct token.

>_WhileStatement &rarr; KW_WHILE Condition KW_DO Statement_

```java
void parseWhileStatement(TokenSet recoverSet) {
  // String is used for error messages and debugging.
  stmt.parse("WhileStatement", Token.KW_WHILE, recoverSet, () -> { // (2)
    // CONDITION_START_SET is the set of tokens which start conditions
    tokens.match(Token.KW_WHILE, CONDITION_START_SET); // (1)
    parseCondition(recoverSet.union(Token.KW_DO));
    tokens.match(Token.KW_DO, STATEMENT_START_SET);
    parseCondition(recoverSet);
  });
}
```

Here, **tokens.match** takes a second argument. This is what tokens are expected to immediately follow a `while`. 

When matching terminals with **(1)**, if the next token is not `while`, it will emit an error message and see if the current token is in the start set. If it _is_ in the set, it assumes the `while` token is missing and will implicitly insert it. If it is not, it will discard the token and repeat. (This is a very local way of recovering.)

The other part is to do with matching non-terminals such as **(2)**. This looks to see if the next token is the `while` keyword. If it is, it executes the given function. If it is not, it will start skipping tokens until either a token is `while` _or_ it finds something in the _recover set_. The recover set is a set of tokens expected to come after the entire while statement. In this case, it gives up and returns a dummy error node.

For **parseCondition**, if it doesn't match a condition, it will skip until a valid condition or anything in the passed recover set (which will also include `do`). This is the set of things which can follow the condition.

Now, consider a parser for a _RelCondition_:

> _RelCondition &rarr; Exp_ [ _RelOp Exp_ ]

```java
void parseRelCondition(TokenSet recoverSet) {
  exp.parse("RelCondition", EXP_START_SET, recoverSet, () -> {
    parseExp(recoverSet.union(REL_OP_SET));
    if (tokens.isIn(REL_OP_SET)) {
      parseRelOp(recoverSet.union(EXP_START_SET));
      parseExp(recoverSet); // because this is optional, not repetition.
    }
  });
}
```

Let's parse factors!
> _Factor &rarr; LPAREN Condition RPAREN_ | _NUMBER_ | _LValue_

```java
ExpNode parseFactor(TokenSet recoverSet) {
  return exp.parse("Factor", FACTOR_START_SET, recoverSet, () -> {
    ExpNode result = null;
    if (tokens.isMatch(Token.LPAREN)) {
      tokens.match(Token.LPAREN); // cannot fail
      result = parseCondition(recoverSet.union(Token.RPAREN));
      tokens.match(Token.RPAREN, recoverSet);
    } else if (tokens.isMatch(Token.NUMBER)) {
      result = new ExpNode.ConstNode(tokens.getLocation(), 
        Predefined.INTEGER_TYPE, tokens.getIntValue());
      tokens.match(Token.NUMBER); // cannot fail
    } else if (tokens.isMatch(Token.IDENTIFIER)) {
      result = parseLValue(recoverSet);
    } else {
      // will never occur because .parse() only calls this code
      // when a FACTOR_START_SET item is found.
      fatal("internal error in parseFactor");
    }
    return result;
  });
}
```

Note that we must use **tokens.match** after building the constant node because it consumes the next number.
