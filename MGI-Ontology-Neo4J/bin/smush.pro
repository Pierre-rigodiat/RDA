:- dynamic smush_del/1.

do_smush(X,[Y|Z]) :-
	edge(name(X),name(Y),type('first'),_), edge(name(X),name(Q),type('rest'),_), 
	assertz(smush_del(X)),
	do_smush(Q,Z).

do_smush(X,[Y]) :-
	edge(name(X),name(Y),type('first'),_), edge(name(X),name('nil'),type('rest'),_),
	assertz(smush_del(X)).	

add_edges_smush(_,[]).
add_edges_smush(T,[V|VS]) :- 
	assertz(edge(name(T),name(V),type('item'),source('computed'))),
	add_edges_smush(T,VS).

retract_smushed_vertex(X) :-
	smush_del(X),
	retract(vertex(name(X),_)),
	retract(edge(name(X),_,_,_)).

smush(A,X,T,L) :-
	edge(name(A),name(X),type(T),_), T \= 'first', T \= 'rest', 
	do_smush(X,L),
	gensym(T,N),
	assertz(vertex(name(N),source('computed'))),
	add_edges_smush(N,L).

smush_all :-
	findall([A,X,T,L], smush(A,X,T,L), _),
	findall(V, retract_smushed_vertex(V), _),
	findall(D, retract(smush_del(D)), _).

	
dump_vertex(V,S) :-
	vertex(name(V),source(S)),
	write('vertex(name(\''), write(V), write('\'),source(\''), write(S), 
	write('\')).'), nl.

dump_vertexes :-
	findall([V,S], dump_vertex(V,S), _).

dump_edge(L,R,T,S) :-
	edge(name(L),name(R),type(T),source(S)),
	write('edge(name(\''), write(L), write('\'),name(\''), write(R), 
	write('\'),type(\''), write(T), write('\'),source(\''), write(S),
	write('\')).'), nl.

dump_edges :-
	findall([L,R,T,S], dump_edge(L,R,T,S), _).

dump_all :-
	dump_vertexes,
	dump_edges.

clean_up :-
	smush_all,
	dump_all.

