---
tags: [Notebooks/COMP4403]
title: Lecture 3 — Context-Free Grammars 2
created: '2020-03-01T22:22:20.182Z'
modified: '2020-03-01T23:50:03.418Z'
---

# Lecture 3 &mdash; Context-Free Grammars 2

Consider a grammar:
$$
\begin{aligned}
L &\to LL \\ 
L &\to ``x" \\ 
L &\to \epsilon
\end{aligned}
$$
The language of this is 
$$
\mathcal L(G) = \{\epsilon, x, xx, xxx, \ldots\}.
$$
This is ambiguous because the expansion of $\epsilon$ could occur anywhere in the string. For example, $x$ has parse trees $L(x)$, $L(L(x), L(\epsilon))$, and more.

To make this unambiguous, we can force the literal $x$ to occur at either the start or end of the production. That is,
$$
\begin{aligned}
L &\to L\ ``x" \\ 
L &\to \epsilon
\end{aligned}
$$
It should be obvious that $\mathcal L(G)$ is unchanged from before, but the grammar is now unambiguous.

## Statement sequences

Consider a sequence of one or more statements separated by semicolons. A possible grammar is
$$
\begin{aligned}
SS &\to S \\ 
SS &\to SS\ ``;"\ S
\end{aligned}
$$
Subtly different, consider a sequence of one or more statements _terminated_ by semicolons.
$$
\begin{aligned}
SS &\to S\ ``;" SS\\
SS &\to SS\ S\ ``;"
\end{aligned}
$$

Some common idioms are things prefixed or suffixed by other things (left and right associative, respectively).
$$
\begin{aligned}
A \to A \alpha \ |\ \beta &\implies \mathcal L(G) = \{\beta, \beta \alpha, \beta \alpha \alpha, \ldots\}\\
A \to \alpha A \ |\ \beta &\implies \mathcal L(G) = \{\beta, \alpha\beta, \alpha\alpha\beta, \ldots\}
\end{aligned}
$$

### If statements

Consider a grammar
$$
\begin{aligned}
S &\to \textit{IfS} \ |\ \ldots \\ 
\textit{IfS} &\to \text{if } C \text{ then } S \text{ else } S \\
\textit{IfS} &\to \text{if } C \text{ then } S
\end{aligned}
$$
However, this is an ambiguous grammar. Take the case $\text{if } C_1 \text{ then if } C_2 \text{ then } S_1 \text{ else } S_2$. The two interpretations are basically 
$$
\text{if } C_1 \text{ then \{ if } C_2 \text{ then } S_1 \text{ \} else } S_2\\
\text{if } C_1 \text{ then \{ if } C_2 \text{ then } S_1 \text{ else } S_2\ \}
$$
Traditionally, programming languages normally take the second one, matching the $\text{else}$ with the closest starting $\text{if}$ statement. This ambiguity is called the "dangling else problem".

Conventionally, we can also avoid the issue by enforcing braces (C-style), indentation (Python), or a terminating keyword $\text{fi}$ (ALGOL 68, Bash).

## Chomsky hierarchy of grammars
Here, nonterminal symbols are uppercase and terminals are lowercase. Greek letters signify possibly empty sequences of terminals or non-terminals.
- **Type 3**: Left (or right) linear grammars: $A \to \epsilon\ |\ aB\ |\ a$, with $B$ in the same form.
- **Type 2**: Context-free grammars: $A \to \alpha$.
- **Type 1**: Context-sensitive grammars: $\beta A \gamma \to \beta \alpha \gamma$.
- **Type 0**: Unrestricted grammars: $\alpha \to \beta$, where $\alpha \ne \epsilon$.

Note that each type is a superset of the previous. Type 3 left linear grammars are, in fact, regular expressions. Type 1 is called context-sensitive because we can only replace $A$ with $\alpha$ when it is surrounded by the appropriate symbols. 

There are some correspondences between these types and more familiar conventions:
- **Type 3**: finite automaton (state machines), regular expressions, left/right linear grammars.
- **Type 2**: pushdown automaton (with a stack), context-free grammar.
- **Type 1**: context-sensitive grammar.
- **Type 0**: unrestricted grammar, Turing machine equivalent, general computation.

## Recursive descent parsing
We will focus on top-down parsing for now, with bottom-up parsing to come later.

We will be using extended BNF (EBNF) to write our grammars. It is always possible to take an ENBF grammar and rewrite it as BNF. It introduces the following syntax:
- $[\ S\ ]$ is for optionals and is equivalent to $\textit{OpS} \to S\ |\ \epsilon$.
- $\{\ S\ \}$ is for zero or more repetitions of $S$ and is equivalent to $\textit{RepS}\to(S)\ \textit{RepS}\ |\ \epsilon$.
- $(\ S\ )$ is for precedence grouping.

### Implementation
We start with terminal symbols, such as identifiers, matching them with `tokens.match(Token.T)`.

For non-terminal symbols, such as $\textit{RelCondition}$, we will write something like `parseRelCondition()`.

To parse a sequence of symbols, such as $S_1S_2\ldots$, we will use `recog(s1); recog(s2);` for some recogniser functions.

For example, to parse $\textit{Factor}\to\textit{LPAREN RelCondition RPAREN}$ we will use 
```java
tokens.match(Token.LPAREN);
parseRelCondition();
tokens.match(Token.RPAREN);
```

For alternatives, we need to be careful about which alternative to choose. In this grammar, it is always possible to choose the correct alternative by at one token. This is not always the case. For $\textit{Factor} \to \textit{LPAREN RelCondition RPAREN}\ |\ \textit{Number}\ |\ \textit{LValue}, we can match it using
```java
void parseFactor() {
  if (tokens.isMatch(Token.LPAREN)) {
    tokens.match(Token.LPAREN);
    parseRelCondition();
    tokens.match(Token.RPAREN);
  } else if (tokens.isMatch(Token.NUMBER)) {
    tokens.match(Token.NUMBER);
  } else if (tokens.isMatch(Token.IDENTIFIER)) {
    parseLValue();
  } else {
    // throw new eXcEPtIoN("yeet");
    error("Syntax error");
  }
}
```

To parse optionals, such as $\textit{RelCondition} \to \textit{Exp } [\ \textit{RelOp Exp}\ ]$, we can use something like
```java
void parseRelCondition() {
  parseExp();
  if (tokens.isIn(REL_OPS_SET)) { // because there are multiple RelOps
    parseRelOp();
    parseExp();
  }
}
```

To parse an if statement of the form
$$
\textit{IfStatement} \to \textit{KW\_IF Condition KW\_THEN Statement }[\textit{ KW\_ELSE Statement }],
$$
we can use
```java
void parseIfStatement() {
  tokens.match(Token.KW_IF);
  parseCondition();
  tokens.match(Token.KW_THEN);
  parseStatement();
  if (tokens.isMatch(Token.KW_ELSE)) {
    tokens.match(Token.KW_ELSE);
    parseStatement();
  }
}
```

We can parse a term of $\textit{Term} \to \textit{Factor }\{\ (\textit{ TIMES | DIVIDE ) Factor }\}$ like
```java
void parseTerm() {
  parseFactor();
  while (tokens.isIn(TERM_OPS_SET)) {
    tokens.match(tokens.isMatch(Token.TIMES) ? Token.TIMES : Token.DIVIDE);
    // we should assert error if token is neither times or divide.
    parseFactor();
  }
}
```

Consider a rule $\textit{Factor} \to \textit{LPAREN Exp RPAREN }|\ \textit{NUMBER}$. We might want it to _evaluate_ a factor as we parse it. We can do that with an extra variable, like
```java
int parseFactor() {
  int result = 0x80808080; // useful useless value.
  if (tokens.isMatch(Token.LPAREN)) {
    tokens.match(Token.LPAREN);
    result = parseExp();
    tokens.match(Token.RPAREN);
  } else if (tokens.isMatch(Token.NUMBER)) {
    result = tokens.getIntValue(); // assumes current token is a number
    tokens.match(Token.NUMBER); // consume and advance to next token
  } else {
    error("Syntax error");
  }
  return result;
}
```
