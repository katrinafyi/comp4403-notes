# Lecture 9 &mdash; Left-Factoring and Left-Recursion Removal

> March 29, 2020

This is important because if we want LL(1) RDP, any grammar with a common left factor between two alternatives or a left-recursion is unsuitable.

## Left factors

Consider 

> _IfStmt_ &rarr; if ( _Cond_ ) _Stmt_ | if ( _Cond_ ) _Stmt_ else _Stmt_

which is unsuitable for RDP with one symbol look ahead because the two alternatives share a common prefix. This can be rewritten as

> _IfStmt_ &rarr; if ( _Cond_ ) _Stmt_ _ElsePart_
> _ElsePart_ &rarr; $\epsilon$ | else _Stmt_

Remark: This still has the dangling else problem, which is resolved in the parser by selecting the else over the empty string. Also, in EBNF, this is equivalent to _IfStmt &rarr;_ if ( _Cond_ ) _Stmt_ [ else _Stmt_ ].

In general, to remove a left factor of the form _A_ &rarr; $\alpha\ \beta ~|~ \alpha\  \gamma$, we can rewrite the production using an additional new non-terminal as

> _A_ &rarr; $\alpha$ _A'_
> _A'_ &rarr; $\beta$ | $\gamma$

## Left recursion

A production of the form _E &rarr; E_ + _T_ | _T_ is unsuitable for recursive descent parsing because the left recursion always leads to itself, an infinite recursion. This production matches T, T+T, T+T+T, .... Then, the grammar can be rewritten as

> _E_ &rarr; _T_ _E'_
> _E'_ &rarr; $\epsilon$ | + _T_ _E'_

which is _E_ &rarr; _T_ { + _T_ } in EBNF.

In general, _A_ &rarr; _A_ $\alpha$ | $\beta$ (which matches a $\beta$ followed by zero or more $\alpha$'s) can be rewritten as 

> _A_ &rarr; $\beta$ _A'_
> _A'_ &rarr; $\epsilon$ | $\alpha$ _A'_

Note the similarities to the left factoring case.

### Multiple (direct) left recursions

The above rewriting rules can be used when $\alpha$ is replaced by $\alpha_1 ~|~ \alpha_2 ~|~ \cdots$ and $\beta$ is $\beta_1 ~|~ \beta_2 ~|~ \cdots$, to rewrite left recursions of the form _A_ &rarr; _A_ $\alpha_1$ | $\cdots$ | _A_ $\alpha_n$ | $\beta_1$ | $\cdots$ | $\beta_m$.

For example, _E_ &rarr; _E_ + _T_ | _E_ &minus; _T_ | _T_ can be rewritten as

> _E_ &rarr; _T_ _E'_
> _E'_ &rarr; $\epsilon$ | + _T_ | &minus; _T_

### Indirect left recursions

Consider the following production for _A_ which has both a direct left recursion and an indirect left recursion.

> _A_ &rarr; _A_ $\alpha_1$ | _B_ $\alpha_2$
> _B_ &rarr; _B_ $\beta_1$ | _C_ $\beta_2$
> _C_ &rarr; _A_ $\gamma_1$ | $\gamma_2$

First, re remove the _direct_ left recursions for _A_ and _B_ with

> _A_ &rarr; _B_ $\alpha_2$ _A'_
> _A'_ &rarr; $\epsilon$ | _A'_ $\alpha_1$
> _B_ &rarr; _C_ $\beta_2$ _B'_
> _B'_ &rarr; $\epsilon$ | $\beta_1$ _B'_
> $C \to A\ \gamma_1~|~\gamma_2$

To replace the indirect left recursion through $B$, we first replace the use of $B$ in the production of $A$ with its definition, then do the same for $C$.

> _A_ &rarr; _C_ $\beta_2$ _B'_ $\alpha_2$ _A'_
> _A'_ &rarr; $\epsilon$ | _A'_ $\alpha_1$
> _B'_ &rarr; $\epsilon$ | $\beta_1$ _B'_
> $C \to A\ \gamma_1~|~\gamma_2$

> _A_ &rarr; $(A\ \gamma_1~|~\gamma_2)$ $\beta_2$ _B'_ $\alpha_2$ _A'_
> _A'_ &rarr; $\epsilon$ | _A'_ $\alpha_1$
> _B'_ &rarr; $\epsilon$ | $\beta_1$ _B'_

Expanding the grouping parentheses, we can now see a direct left recursion which we rewrite as usual.

> _A_ &rarr; $A\ \gamma_1\ \beta_2 B'\ \alpha_2\ A' ~|~ \gamma_2\ \beta_2\ B'\ \alpha_2\ A'$
> _A'_ &rarr; $\epsilon$ | _A'_ $\alpha_1$
> _B'_ &rarr; $\epsilon$ | $\beta_1$ _B'_

> $$
> \begin{aligned}
> A &\to \gamma_2\ \beta_2\ B'\ \alpha_2\ A'\ A''\\
> A'' &\to \epsilon ~|~ \gamma_1\ \beta_2 B'\ \alpha_2\ A'\ A''\\
> A' &\to \epsilon ~|~ A'\ \alpha_1 \\ 
> B' &\to \epsilon ~|~ \beta_1\ B'
> \end{aligned}
> $$
>
> 