lower([],_,[]).
lower([Head|Tail], V, [Head|LowerTail]) :- 
    Head < V, 
    lower(Tail, V, LowerTail).
lower([Head|Tail], V, LowerTail) :- 
    Head >= V, 
    lower(Tail, V, LowerTail).

upper([],_,[]).
upper([Head|Tail], V, [Head|UpperTail]) :- 
    Head > V, 
    upper(Tail, V, UpperTail).
upper([Head|Tail], V, UpperTail) :- 
    Head =< V, 
    upper(Tail, V, UpperTail).

equal([],_,[]).
equal([Head|Tail], V, [Head|EqualTail]) :- 
    Head == V, 
    equal(Tail, V, EqualTail).
equal([Head|Tail], V, EqualTail) :- 
    Head \= V, 
    equal(Tail, V, EqualTail).

qsort([],[]).
qsort([V|Tail], Sorted) :-
    lower(Tail, V, Lower),
    equal([V|Tail], V, Equal),
    upper(Tail, V, Upper),
    qsort(Lower, SortedLower),
    qsort(Upper, SortedUpper),
    append(SortedLower, Equal, SortedLowerEqual),
    append(SortedLowerEqual, SortedUpper, Sorted).
