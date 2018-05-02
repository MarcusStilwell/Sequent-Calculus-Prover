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


## Examples

For $\neg A \vee \neg B$
```
Hypotheses: ~Av~B
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

For $(G \rightarrow D)  \rightarrow ((G \rightarrow (F \vee D)) \wedge ((F \wedge G  )\rightarrow D))$
```
Hypotheses: 
Conclusion: (G->D)  -> ((G->(FvD)) ^ ((F^G  )->D))
.
.
.
tree ommited
.
.
.
Valid: True
```

For $(G \rightarrow D)  \rightarrow ((G \rightarrow (F \vee D)) \wedge ((F \wedge G  )\rightarrow (\neg F \vee \neg G)))$

```
Hypotheses: 
Conclusion: (G->D)  -> ((G->(FvD)) ^ ((F^G  )->(~F v ~G)))
.
.
.
tree ommited
.
.
.
Valid: False
```