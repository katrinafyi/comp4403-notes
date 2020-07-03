---
tags: [Notebooks/COMP4403]
title: Tutorial 3 — RDP Exercise
created: '2020-03-10T02:15:32.353Z'
modified: '2020-03-10T02:32:08.663Z'
---

# Tutorial 3 &mdash; RDP Exercise

> _RepeatStatement → KW_REPEAT StatementList KW_UNTIL Condition_

```java
void parseRepeatStatement() {
  tokens.match(Token.KW_REPEAT);
  parseStatementList();
  tokens.match(Token.KW_UNTIL);
  parseCondition();
}
```

```java
void parseRepeatStatement(TokenSet recoverSet) {
  stmt.parse("RepeatStatement", Token.KW_REPEAT, recoverSet, () -> {
    tokens.match(Token.KW_REPEAT, recoverSet.union(STATEMENT_START_SET));
    parseStatementList(recoverSet.union(Token.KW_UNTIL));
    tokens.match(Token.KW_UNTIL, recoverSet.union(CONDITION_START_SET));
    parseCondition(recoverSet);
  });
}
```

```java
StatementNode parseRepeatStatement(Tokenset recoverSet) {
  return exp.parse("RepeatStatement", Token.KW_REPEAT, recoverSet, () -> {
    Location loc = tokens.getLocation();
    tokens.match(Token.KW_REPEAT, recoverSet.union(STATEMENT_START_SET));
    StatementNode body = parseStatementList(recoverSet.union(Token.KW_UNTIL));
    tokens.match(Token.KW_UNTIL, recoverSet.union(CONDITION_START_SET));
    ExpNode condition = parseCondition(recoverSet);
    return new StatementNode.RepeatNode(loc, body, condition);
  });
}
```
