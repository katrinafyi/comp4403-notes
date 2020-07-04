---
title: Shift/Reduce Parsing
author: Kenton Lam
date: Saturday July 4, 2020
---

This is a summary of the shift/reduce category of parsers, including LR(0), LR(1) and LALR(1). Written by Kenton Lam. Based on BottomUp-handout.pdf.

## Overview

Shift/reduce parsers work bottom-up; from the input sequence, they build up a parse tree ending at the start symbol. They use a stack and have three actions:

- _shift_ which pushes the next symbol onto the stack,
- _reduce_ $N \to \alpha$ when the top of the stack is $\alpha$ which reduces it to $N$, and
- _accept_ when the stack contains just the start symbol and there is no more input.

Different strategies for deciding between shifting or reducing give rise to different parser schemes, such as LR(0), SLR(1), LR(1), and LALR(1).

## LR(0) parsers

This is left-to-right, rightmost derivation, zero symbol lookahead. 

An **LR(0) parsing item** is of the form $N \to \alpha \bullet \beta$ which means we are trying to match $N$ and have currently matched $\alpha$. $N$ is a non-terminal, and $\alpha$ and $\beta$ are possibly empty terminal/non-terminal sequences such that $N \to \alpha \beta$ is a production.

### LR(0) parsing items

An **LR(0) parsing automaton** (or state machine) consists of a finite set of *states*, each with a set of LR(0) parsing items. The **kernel item**, used to generate the items of the initial state, is $S' \to \bullet S$ where $S$ is the start symbol.

#### Derived items

If a state has an item of the form $N \to \alpha \bullet M \beta$, where $M \to \alpha_1 \mid \cdots \mid \alpha_m$, this state also contains the **derived items** of
$$
M \to \bullet \alpha_1, \ldots, M \to \bullet \alpha_m.
$$
This is because at this state, we can start matching an alternative of $M$. It is important to note that these are in the _same state_ as the original item.

#### Goto states

If a state $s_0$ has an item of the form $N \to \alpha \bullet x \beta$ where $x$ is any symbol, then there is a transition from $s_0$ to a **goto state** $s_1$ on $x$. This new state $s_1$ has a kernel item of the form $N \to \alpha x \bullet \beta$, used to generate its derived items.

If multiple items in $s_0$ have $x$ to the right of $\bullet$, the goto state $s_1$ contains all those items with $\bullet$ moved after the $x$. If states have the same kernel item, they can be treated as equivalent.

### LR(0) parsing actions

Once we have the states and their items, we can determine what action each state represents. Each state always performs the same action.

- $N \to \alpha \bullet a\beta$ where $a$ is a terminal indicates a **shift** action.
- $S' \to S\bullet$ indicates the state has an **accept** action.
- $N \to \alpha \bullet$ (where $S'\ne N$) indicates a **reduce** $N \to \alpha$ (the production is part of the action name).

A shift at EOF is an error, as is accept when there is input remaining.

### LR(0) conflicts

A conflict occurs if a state has two different actions as derived above. Note that all _shift_ actions are the same, so there is no shift/shift conflict. Apart from this, any action can conflict with any other action.

A grammar is called LR(0) if its parsing automaton has no parsing action conflicts.

## LR(1) parsers

A LR(1) parser is left-to-right, rightmost derivation, using one symbol lookahead.

An **LR(1) parsing item** is of the form $[N \to \alpha \bullet \beta, T]$, made up of an LR(0) parsing item and a _lookahead set_ of terminal symbols $T$ (possibly containing $\$$). This indicates that $N$ is currently being matched in a context where $T$ can follow $N$.

## LR(1) parsing items

An **LR(1) parsing automaton** is a set of states, where each state has a set of LR(1) parsing items. The initial state's kernel item is $[S' \to \bullet S, \left\{ \$ \right\}]$ because only EOF can validly follow the start symbol.

### Derived items

Suppose a state has an LR(1) parsing item of $[N \to \alpha \bullet M \beta, T]$. The LR(0) item is derived identically to ordinary LR(0). The new lookahead set depends on whether $\beta$ is nullable. 

Specifically, if $[N \to \alpha \bullet M \beta, T]$ and $M \to \alpha_1 \mid \cdots \alpha_m$, then the derived items are
$$
[M \to \alpha_1, T'],\ \ldots\ ,\ [M \to \alpha_m, T'].
$$
If $\beta$ is nullable, $T' = \operatorname*{First}(\beta)$ otherwise $T' = T \cup\operatorname*{First}(\beta) \setminus \left\{ \epsilon \right\} $.

> **Important:** This needs to be repeated multiple times to get the correct lookahead set, possibly deriving from the same symbol many times.

### Goto states

Goto states work identically to LR(0). The lookahead set is unchanged.

These should be computed after the items have been fully derived above.

## LR(1) parsing actions

While LR(0) actions did not depend on the input token, LR(1) actions can. There are the same three actions, but deciding between them is more specific.

- $[N \to \alpha\bullet a \beta, T]$ where $a$ is a terminal indicates a **shift on $a$** action,
- $[S' \to \bullet S, \left\{ \$ \right\}]$ has an **accept** action on EOF, and
- $[N \to \alpha \bullet, T]$ with $N \ne S'$ has a **reduce $N \to \alpha$ on $x$** action for all $x \in T$.

If no action matches the current state and input, it is a parse error.

### LR(1) conflicts

The conflicts are much the same as LR(0) but they only occur when there are different actions on the same terminal symbol.

A grammar is LR(1) if there is no parsing conflict in its LR(1) parsing automaton.

## LALR(1) parsers

A LALR(1) parser is just a LR(1) but states with the same set of LR(0) items are merged. The new lookahead set for each item is the unions of the original lookahead sets for that item.