/*Rules*/
and(A,B):- is_true(A), is_true(B).

or(A,B):- is_true(A) ; is_true(B).

lhc(and(and(A,B))C):-
  and(A,C).
rhc(and(C,and(A,B))):-
  and(C,A)
  and(C,B).
lhd(and(or(A,B)C)):-
  and(or(A,C),or(B,C)).
rhd(and(C,or(A,B))):-
  and(C,or(A,B))
la():-

ra():-

lw():-

rw():-

lC():-

rc():-
