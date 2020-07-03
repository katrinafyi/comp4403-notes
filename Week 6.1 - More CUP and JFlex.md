# Week 6.1 &mdash; More Java-CUP and JFlex Examples

We will consider a calculator extended with "let" expressions. It looks something like this:

> 2 + let $x$ = 3 in let $y = x+x$ in $x+y$ end end

Consider the CUP code handling a let expression:

```java
   |  KW_LET IDENTIFIER:id EQUAL E:def 
      {:
         if( debug ) {
             System.out.println( "  Adding " + id + " = " + def );
         }
         symtab.add( id, def );
      :}
      KW_IN E:e KW_END
      {:
         RESULT = e; 
         String removed = symtab.removeDef();
         if( debug ) {
             System.out.println( "  Removed " + removed );
         }
      :}
```

Note that we can split up the Java code so the symbol is inserted at the define token and removed after the end token. This allows the expression `E:e` to utilise the defined value but not anything after it.

Ian has implemented a basic stack as a linked list to handle the symbol table entries. This has the benefit of allowing inner identifiers to shadow later identifiers, at the cost of slower access for identifiers defined earlier.

Tutorial 6's compiler is very similar to the compiler of the next assignment. It uses Java-CUP and code generation for a stack machine instead of the handwritten parser of assignment 1.

Note that JFlex matches the longest token, then tokens top to bottom.

In CUP, note that in a production rule like `LValue ::= IDENTIFIER:id` defines variables `idxleft` and `idxright` as the indices of left and right of the IDENTIFIER token.