---
attachments: [Clipboard_2020-03-14-10-30-12.png, Clipboard_2020-03-14-10-31-47.png]
tags: [Notebooks/COMP4403]
title: Lecture 6 — Static Semantic Analysis
created: '2020-03-13T23:56:30.609Z'
modified: '2020-03-14T00:31:53.289Z'
---

# Lecture 6 &mdash; Static Semantic Analysis

At the top level, a program is just a block and a block contains declarations then the main body. Declarations are a mapping from an identifier to a declaration.

Statements are assignments, writes, reads, calls, if, while, or statement lists.

Expressions can be numbers, lvalues, unary operators, binary operators, or a 'narrow' which narrows an expression to a subrange.

We need to know the types of all the identifiers as they're declared. This is represented as a mapping, or symbol table. We also need to know the types of operators, such as $+ : \mathbb Z \times\mathbb Z \to \mathbb Z$.

If we declare $x$ to be an integer, internally we know it is a "ref int" or a reference to an integer. 

The symbol table stores ConstEntry, TypeEntry, VarEntry, or ProcEntry. For example, the code
```
const C = 42;
type S = [-C..C];
var b : boolean;
    y : S;
```
has the following symbol table
> C &#8614; ConstEntry(int, 42)
> S &#8614; TypeEntry(subrange(int, -42, 42))
> b &#8614; VarEntry(ref(boolean))
> y &#8614; VarEntry(ref(subrange(int, -42, 42)))

### Type inference rules

Something like $\textit{syms} ~\vdash n : \text{int}$ (**integer value**) means that given a symbol table _syms_, any number is of type int.

![](assets/Clipboard_2020-03-14-10-31-47.png)

There are other rules in the PL0-SSemantics.pdf document. Note that narrowing subranges may require a runtime check or more advanced static analysis.

![](assets/Clipboard_2020-03-14-10-30-12.png)
