---
title: Recursive Descent Parsing
author: Kenton Lam
date: Saturday July 4, 2020
---

This is an overview of context-free grammars, recursive descent parsing, and syntax error recovery. It is based on the CFG-handout.pdf, RecursiveDescentParsing.pdf, and FirstFollow-handout.pdf handouts. Written by Kenton Lam.

## Grammars

Here, nonterminal symbols are uppercase and terminals are lowercase. Greek letters signify possibly empty sequences of terminals or non-terminals.

- **Type 3**: Left (or right) linear grammars: $A \to \epsilon\ |\ aB\ |\ a$, with $B$ in the same form.
- **Type 2**: Context-free grammars: $A \to \alpha$.
- **Type 1**: Context-sensitive grammars: $\beta A \gamma \to \beta \alpha \gamma$.
- **Type 0**: Unrestricted grammars: $\alpha \to \beta$, where $\alpha \ne \epsilon$.

Note that each type is a superset of the previous. Type 3 left linear grammars are, in fact, regular expressions. Type 1 is called context-sensitive because we can only replace $A$ with $\alpha$ when it is surrounded by the appropriate symbols. In type 0, anything goes.

There are some correspondences between these types and more familiar conventions:

- **Type 3**: finite automaton (state machines), regular expressions, left/right linear grammars.
- **Type 2**: pushdown automaton (with a stack), context-free grammar.
- **Type 1**: context-sensitive grammar.
- **Type 0**: unrestricted grammar, Turing machine equivalent, general computation.

### BNF and EBNF

**Backus Naur form** (BNF) allows us to define context-free grammars in terms of productions. It only allows productions of the form $N \to \alpha_1 \mid \cdots \alpha_n$, where $\alpha_i$ is a (possibly empty) sequence of terminals and non-terminals.

**Extended Backus Naur form** (EBNF) is a notational convenience and extends BNF with

- optional constructs written as $[\ \alpha\ ]$,
- repetition (zero or more times) as $\left\{ \ \alpha\ \right\}$, and
- grouping with $(\ \alpha\ )$.

EBNF does not extend the capabilities of the language itself and is only to simplify defining productions. There are simple rules for rewriting these as BNF.
$$
\begin{aligned}
\textit{OptS}\to[\ S\ ] &\implies \textit{OptS} \to S\mid \epsilon \\ 
\textit{RepS} \to \left\{ \ S \ \right\} &\implies \textit{RepS} \to S \ \textit{RepS} \mid \epsilon \\ 
\textit{GrpS} \to (\ S\ ) &\implies \textit{GrpS} \to S
\end{aligned}
$$

## Context-free grammars

A **context-free grammar** consists of

- a finite set of terminal symbols $\Sigma$,
- a finite, non-empty set of nonterminal symbols (disjoint from the terminals),
- a finite, non-empty set of productions $A \to \alpha$, where $A$ is a nonterminal and $\alpha$ is a possibly empty sequence of nonterminal or terminal symbols, and
- a start symbol which is nonterminal.

The "context-free" is because the left-hand side of a production cannot contain other symbols.

- A **direct derivation** step is a transformation of the form $\alpha N \beta \Rightarrow \alpha \gamma \beta$, assuming there is a production $N \to \gamma$. 
- A **derivation** is zero or more direct derivation steps, and is written $\alpha \overset * \Rightarrow \beta$. 

- A sequence $\alpha$ is **nullable** if $\alpha \overset * \Rightarrow \epsilon$.
- The **formal language** of a grammar $G$ is the set of all sequences derivable from the start symbol $S$, denoted $\mathcal L(G) = \left\{ t \in \operatorname*{seq}\Sigma \mid S \overset * \Rightarrow t \right\}$.
- A **sentence** $t$ is a sequence of terminals derivable from $S$.
- A **sentential form** is a sequence of terminals or non-terminals derivable from $S$.

### Ambiguous grammars

#### Associativity

A grammar is **ambiguous** if there exists a sentence $t$ with multiple parse trees. To remove ambiguity, we can enforce left or right associativity via (respectively):
$$
\begin{aligned}
E &\to E \text{ ``-" }T & E &\to T \text{ ``-" } E \\ 
E &\to T & E  &\to T \\ 
T &\to N & T &\to N
\end{aligned}
$$

#### Precedence

A grammar could also be ambiguous because the precedence is unspecified. This can be fixed by moving the higher precedence expressions into new productions, so the root only has the lowest precedence operators. For example,
$$
\begin{aligned}
E &\to E + T \mid T \\ 
T &\to T * F \mid F \\ 
F &\to N \mid (~ E~)
\end{aligned}
$$
This treats $+$ as lower precedence than $*$ and allows parentheses to have highest precedence of all. Intuitively, the alternatives of a production exist at the same "level" of precedence. 

#### Recursion

The grammar $L \to LL \mid x \mid \epsilon$ is ambiguous because the expansion of $\epsilon$ could occur anywhere. To mane this unambiguous, we force the literal $x$ to occur at either the start or end, for example
$$
L \to L\,x \mid \epsilon.
$$
This is equivalent because $\mathcal L(G)$ is unchanged but it is now unambiguous.

## Recursive descent parsing

If we want to do LL(1) recursive descent parsing (which we do), any grammar with a common left factor between alternatives or left recursion is unsuitable. These lead to ambiguity in possible alternatives, and infinite recursion (respectively).

### Left factors

For example, 
$$
\textit{IfStmt} \to  \text{if}\ (\ \textit{Cond}\ )\ \textit{Stmt} \mid \text{if}\ ( \textit{Cond} \ )\ \text{else}\ \textit{Stmt}
$$
is unsuitable because of the common left prefix between alternatives. To resolve this, we factor out the prefix and write 
$$
\textit{IfStmt} \to  \text{if}\ (\ \textit{Cond}\ )\ \textit{ElsePart},\quad \textit{ElsePart}\to \epsilon \mid  \text{else}\ \textit{Stmt}.
$$
In general, to remove a left factor, we rewrite a production like so:
$$
A \to \alpha \beta \mid \alpha \gamma \quad\implies\quad A \to \alpha\ A',\ A' \to \beta \mid \gamma.
$$
Note that this is $A \to \alpha\ (\beta \mid \gamma)$ in EBNF.

### Direct left-recursion

A production like $E \to E + T \mid T$ causes left recursion because the RDP will always attempt to expand $E$ while parsing $E$. Looking at the language, this production derives $\left\{ T, T+T, \ldots \right\}$. We can rewrite this by forcing the leftmost term to be a simplified non-terminal, like
$$
E \to T\ E', \quad E' \to \epsilon \mid  +\ T\ E'
$$
or $E \to T \left\{+T \right\}$ in EBNF. In general, we force the base case of the left-recursion to happen first, otherwise we go to a new non-terminal, so
$$
A \to A\ \alpha \mid \beta \quad \implies \quad A \to \beta\ A',\ A' \to\epsilon\mid \alpha\ A'
$$
which is $A \to \beta \left\{ \alpha \right\}$ in EBNF.

This can be extended to rewrite left-recursion of the form $A \to A \alpha_1 \mid \cdots \mid A \alpha_n \mid \beta_1\mid \cdots \mid\beta_m$ in much the same way by using grouped alternatives in place of $\alpha$ and $\beta$.

### Indirect left-recursion

Indirect left-recursion poses the same problems but is trickier to solve. The process goes something like this:

1. Remove direct left-recursion.
2. Replace productions which cause left-recursion by their definitions, then remove the production.
3. Repeat previous step until we see a direct left recursion.
4. Repeat from 1 as necessary.

### First and follow sets

In recursive descent parsing, we need to choose between alternatives based on the current token and the next token (one symbol lookahead). To do this, we construct two sets for each production:

- the **first set**, the tokens which each alternative can begin with, and
- the **follow set**, the tokens which can follow a construct.

#### First set

The first set of a construct $\alpha$ is denoted $\operatorname*{First}(\alpha)$ and contains the terminals which can start $\alpha$ and $\epsilon$ if $\alpha$ is nullable. The first set of a sequence is constructed from the union of the first sets of its _nullable_ prefixes except $\epsilon$. For non-nullable $\alpha$,
$$
\operatorname*{First}(\alpha)=\left\{ \text{a} \in \operatorname*{terminals} \mid \exists\ \beta : \alpha \overset * \Rightarrow \text a\,\beta \right\}
$$
If the entire sequence $\alpha$ is nullable, $\epsilon$ is added to the first set.

#### Follow set

By definition, a non-terminal $N$ is followed by a terminal $a$ if there exists a derivation from $S\$$ in which $a$ follows $N$. Thus,
$$
\operatorname*{Follow}(N) = \left\{ \text a \in \text{terminals} \mid \exists \ \alpha, \beta : S\,\$\overset *\Rightarrow \alpha\, N\,\text  a\,\beta \right\}
$$
where $\beta$ is a nullable sequence.

As a consequence of this definition, a follow set _may_ contain $\$$, first sets _never_ contain $\$$, and follow sets _never_ contain $\epsilon$.

There are some simple rules which can be used for calculating follow sets.

- $\$ \in \operatorname*{Follow}(S)$ for all $S$,
- if $A \to \alpha N \beta$, then $\operatorname*{First}(\beta)\setminus \left\{ \epsilon \right\} \subseteq \operatorname*{Follow}(N)$ (i.e. anything that starts $\beta$ could follow $N$), and
- if $A \to \alpha N \beta$ and $\beta$ is nullable, then $\operatorname*{Follow}(A) \subseteq \operatorname*{Follow}(N)$ (i.e. anything that follows $A$ could follow $N$).

### LL(1) grammars

A grammar is **LL(1)** if for each non-terminal $N$ where $N \to \alpha_1 \mid \cdots \mid \alpha_n$,

- the first sets are pairwise disjoint: $i \ne j \implies \operatorname*{First}(\alpha_i)\cap \operatorname*{First}(\alpha_j) = \emptyset$, and
- if $N$ is nullable, $\operatorname*{First}(N)$ and $\operatorname*{Follow}(N)$ are disjoint.

Together, this lets us uniquely select an alternative based on the next token. Note that the first sets being pairwise disjoint means at most one alternative can be nullable. Given an LL(1) grammar, during recursive descent parsing the current token is either: 

- in the first set of just one alternative and that alternative is chosen, or
- in the Follow set of N, and the (unique) nullable alternative for N is chosen,
- otherwise there is a syntax error.

### Syntax error recovery

Syntax error recovery attempts to recover from simple programmer errors. This is done by local error recovery on a single token and synchronising the input stream at the start of each parse method.

#### Local error recovery

This is the error recovery done by $\texttt{tokens.match()}$. It handles the following cases:

- a single token missing from input,

- an additional invalid token inserted into the input,

- a single invalid token replacing the expected token.

To do this, the parse method for a token $T$ takes a "recover set" which is the set of tokens possibly following $T$ in the context it's being matched in. When encountering an invalid token $I$  when we are trying to match $T$, three cases can occur:

- $I$ is in the recover set and we assume $T$ was omitted,
- $I'$ (the token following $I$) is $T$, so we assume $I$ was erroneously inserted and matches on $I'$, or
- $I'$ is still not $T$, we assume $I$ erroneously replaced $T$ in the input.

#### Parse synchronisation

This concerns error recovery of $\texttt{parseStatement()}$ and similar methods. This synchronises the current token both before and after a parse method is run. Before parsing a non-terminal $N$, it ensure that the current token $T$ 

- can start $N$ (i.e. is in $\operatorname*{First}(N)$), or
- if $N$ is nullable, $T$ can follow $N$ (i.e. is in recover set).

Before parsing, the error recovery discards tokens until the current token can start $N$ and then executes the parse, or until the current token is in the recover set of $N$ then it assumes $N$ was skipped and returns an error node.

After parsing, it discards until the current token is in the recover set, reporting error messages if one or more tokens were discarded.

The $\texttt{parseN()}$ pass their recover set unioned with extra symbols to other $\texttt{parseM()}$ methods, but only use specific sets for $\texttt{tokens.match()}$ recover sets. For example:

```java
void parseWhileStatement(TokenSet recoverSet) {
    tokens.match(Token.KW_WHILE, CONDITION_START_SET);
    parseCondition(recoverSet.union(Token.KW_DO));
    tokens.match(Token.KW_DO, STATEMENT_START_SET);
    parseStatement(recoverSet);
}
```

