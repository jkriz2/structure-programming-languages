parent(david, greg).
parent(pauline, greg).
parent(david, kim).
parent(david, steph).
parent(greg, katie).

parent(P,C) :- sibling(B,C), parent(P,B), B\=C.

sibling(A,B) :- parent(X,A), parent(X,B), A\=B.


grandparent(Grandparent, Grandchild) :- parent(Grandparent,X),parent(X,Grandchild).
