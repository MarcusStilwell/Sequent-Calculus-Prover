# Sequent-Calculus-Prover

## Usage
Symbols used are 
- v for conjunction
- ^ for disjunction
- ~ for negation
- ! for false
- -> for impication
- A-Z for literals

When entering formulas, use of brackets is highly advised, as no order of operations are enforced. Formulas where more than 2 literals are used require brackets, ie.

```AvBvC ```
will not be parsed properly, while

```(AvB)vC``` 
would be.

In general, the prover will try to match, in the following order (where op is the primitive)
1.  A  op  B  (where A and B are literals).
2. (F) op (G) (where F and G are formulas).
3. (F) op  G  (where F and G are formulas, matched greedily).
4.  F  op (G) (where F and G are formulas, matched greedily).


## Limitations
- Clauses are checked against the rules from left to right, and so no smart matching is done to reduce branches.
- No order of operations implemented.
- When printing the tree, formating is very limited.
- When using negation, brackets need to be used around the negation, ie. ~A would be (~A) for it to be parsed correctly (it will occasionally work without brackets, but not all the time).


## Examples

For \~Av~B => ~(A^B)
```
Hypotheses: (~A)v(~B)
Conclusion: ~(A^B)
.
.
.
tree ommited
.
.
.
Valid: True
```

For A->B => ~AvB
```
Hypotheses: A->B
Conclusion: (~A)vB
.
.
.
tree ommited
.
.
.
Valid: True
```


For A->B => Av~B
```
Hypotheses: A->B
Conclusion: Av(~B)
.
.
.
tree ommited
.
.
.
Valid: True
```

For => (G->D) -> ((G->(FvD)) ^ ((F^G  )->(~F v ~G)))
```
Hypotheses: 
Conclusion: (G->D) -> ((G->(FvD)) ^ ((F^G  )->(~F v ~G)))
.
.
.
tree ommited
.
.
.
Valid: False
```

For => (G->D) -> ((G->(FvD)) ^ ((F^G  )->D))
```
Hypotheses: 
Conclusion: (G->D) -> ((G->(FvD)) ^ ((F^G  )->D))
.
.
.
tree ommited
.
.
.
Valid: True
```

For => ((G->(FvD)) ^ ((F^G)->D)) -> (G->D)
```
Hypotheses: 
Conclusion: ((G->(FvD)) ^ ((F^G)->D)) -> (G->D)
.
.
.
tree ommited
.
.
.
Valid: True
```

