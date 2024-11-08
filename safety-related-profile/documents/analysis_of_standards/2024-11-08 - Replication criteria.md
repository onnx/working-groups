Dans l'expression des propriétés de robustesse, réexprimer les choses de la façon suivante : "Complying with MLMD ensures that..."

Discussion sur les propriétés de réplication 

- Utilisation du terme "sémantique"
	- Est-ce pertinent ? 
		- Oui, si on cherche la définition de "sémantique" dans le domaine informatique pour un langage donné 
	- Est-ce compréhensible?
	
	# Exact replication 
	
	
	"sufficient details on the ML model semantic"
		What does "details" mean here? 
		"contain[ing] sufficient details does not ensure that the semantic will be preserved. It shall provide sufficient "details" to allow the implementer to preserve the semantic. 
		
		The definition is somewhat reflexive in the senses that Even a weak semantic can be preserved. 
		
		What is the "ML model"?
		
		Providing a sufficiently accurate 
	
		The definition states that "an exact replicaton criterion may be the direct and faithfull implementation of the ML Model description". 
		Written as a property, this means that an exact replication criterion could be 
		"The implementation directly and fully implements the ML Model description"  
		What "directly" means is not clear. It could be interpreted as a traceability property such as "all elements of the MLMD are traceable to the implementation of the MLMD and reciprocally". In practice, this coul dmeans that we expect each element of the MLMD ("graph", "node",...) to be found in the implementation.
		In that sense, an implementation "exactly replicate" the MLMD if there is some sort of bijection between the set of elements of the MLMD and the sets of elements of the implementation of the MLMD.
		
		Another interpretation could be that the function $f_imp$ realized by the implementation of the MLMD is the same as the function $f$ defined by the MLMD, i.e., for any input $x$ in the domain of the function, the $f(x)=$f_imp(x)$.  
		
		The last part of the definition makes things even less clear in the sense that it could be interpreted as "exact replication actually means that the performance, generalization, stability and robustness" of the implementation are the same of the MLMD model. Note that (i) talking about the robustness of the "MLMD model" is difficult to interpret in practice without indicating what will be the strutcure that will interpret the model. Stated differently, nobody can evaluate the perfomance of a MLMD model buy looking at it: it must be executed to obtain 
		these figures... 
		Then, the definition identifies 4 quantities (performance, generalization, ...)". Is this list exhaustive? and what do we mean exactly by "performance" (there are quite a few performance metrics in ML) or "robustness" (local? global?). Those 4 metrics could be understood as examples of what one could want to achieve thanks to a "faithful" replication of the structure of the MLMD. 
		
		Approximate definition 
		

