lower([],_,[]).
lower([Head|Tail], V, [Head|LowerTail]) :- 
    Head =< V, 
    lower(Tail, V, LowerTail).
lower([Head|Tail], V, LowerTail) :- 
    Head > V, 
    lower(Tail, V, LowerTail).

upper([],_,[]).
upper([Head|Tail], V, [Head|UpperTail]) :- 
    Head > V, 
    upper(Tail, V, UpperTail).
upper([Head|Tail], V, UpperTail) :- 
    Head =< V, 
    upper(Tail, V, UpperTail).

qsort([],[]).
qsort([V|Tail], Sorted) :-
    lower(Tail, V, Lower),
    upper(Tail, V, Upper),
    qsort(Lower, SortedLower),
    qsort(Upper, SortedUpper),
    append(SortedLower, [V | SortedUpper], Sorted).

