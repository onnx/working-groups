## Participants
Mariem, Augustin, Michele, Pierre, Cyril, Yrina, Filippo, Loïc, Jean, Eric [ed]

## Dissemination 
Participants + SONNX.

## Meeting objective
- During the DeepGreen meeting at ONERA Toulouse, it appeared that there could be some interesting and useful collaboration between [DeepGreen](https://deepgreen.ai/) (esp. the work done on the [AIDGE platform](https://eclipse.dev/aidge)), the [SONNX initiative](https://github.com/ericjenn/working-groups/blob/ericjenn-srpwg-wg1/safety-related-profile), and other work done on formal specification and verification.\ A summary of the discussions is given at the end of these minutes. 
- Today's meeting was aimed at identiying ways to collaborate, define a common objective and  actions to reach it.

## Minutes

- Overview: We consider that a SONNX-aware backend coul dbe integrated into AIDGE. This backend  would be able to generate an implmeentation compliant with the SONNX model. This implementation would be a Reference Implementaion (RI).

- The RI could be used as a test oracle to verify some end-user's own implementation.
  
- The RI is not absolutely required in the sense that someone may well 	
	- develop its own implementation from the SONNX model and 
	- demonstrate (using formal method, test, etc.) that his/her implementation comply with the spec without using the RI.
	Nevertheless, having a reference implementation facilitate the implementation of a test strategy. 

- The overall approach should be somewhat similar to what is currntly done at Airbus using SCADE applicatons.
  
- The RI does not need to be efficient. It has to be simple and traceable.
- Verifying an optimized implementation would be a "plus". However, 
	- an optimized implementation is often optimized with respect to some specific target, so we would need to have several "optimized" implementation 
	- having an optimal implementation is not necessary for verification purposes (<off-meeting except if testing time is a problem/>)
	- verifying an optimized implementation is probably more complex than verifying a "simpler" one (<off-meeting "simpler" could be related to the capability to verify it formally... />
 
- We need to have a clear view of what we expect / need from the formal specification (what are the properties at stake?). 
	- This suject will be adressed during Nov. 29th meeting (<off-meeting which is a bit late... />
	- The question of numerical errors, specification of numerical computation is another subject to be clarified (<off-meeting: this will be adressed during the next SONNX meeting, Nov. 6th />
 
- In order estimate the feasibibity of a formal specification, the "type" of provable properties, the effort, we do need to take a concrete example. In particular, we need to have access to the operators' code.
	- [ ] (Loïc et al) Analyse the operators in order to determine the feasibility of a formal specification

- We have to consider the benefit / cost ratio of using formal verification considering that (i) we do not target the highest DAL, (ii) other methods can be used to reach acceptable level of assurance. The idea is to use FM is it actually facilitate verification (<off-meeting: which means that we have to be clear on the verification objectoves />

- The question of FP computations is particularly difficult. (<off-meeting: When are automated verification of FP computations applicable? />

- Two case studies were proposed: 
	- ACAX Xu, using operators MatMul, Add,and Relu
	- MNIST, using operators Conv, Relu, maxpool, Gemm. This is one example given in the [AIDGE github](https://eclipse.dev/aidge/source/Tutorial/export_cpp.html).
	
- ACETONE's code could be a good starting point for the reference implementation (it is open source and is available at https://github.com/onera/acetone). 
- Some operators have also been formally specified as part of Yrna's thesis (to be published). If possible, it would be nice to start from / use Yrina's work.
- [ ] (Yrina) Clarify what could be available to support this PoC with Claire and Filippo
- [ ] (Yrina) If possible, provide access to the specification of operators.

- A target objective is to develop a first PoC, applied on a simple example, a present it during  DeepGreen's meeting in March.
- The major steps woud be 
	- Select a case study
	- Develop the "replication specification" for the case study 
	- Develop the description all operators used in this case study.
	- Develop the formal specification of all operators used in this case study.
	- Develop a C implementation of these operators. 
	- Ensure or demonstrate that they comply with their specification
	- Integrate the operators in AIDGE
	- Specify the graph execution semantics
	- Develop a C implementation of the scheduler. 
	- Ensure or demonstrate that it complies with the specification.
	- Integrate the scheduler in AIDGE.
	- Generate a complete RI of the SONNX model
	- Build a verification case demonstrating that the model implementation (operators + graph) complies with the model specification (SONNX model), accoding to the "replication specification"
	
- [ ] (Eric+Jean) Elaborate a development plan


## Eric's mail (in French)

### - Implémentation de référence
L'objectif central du WG SONNX est de donner les moyens de décrire un graphe de façon compréhensible, non ambigüe, etc. Cependant, en pratique, il va être difficile de vérifier qu'une implémentation est conforme à son modèle d'entrée sur une base purement formelle : il est plus que probable que nous soyons obligés de reposer sur une approche de test.

Or, pour réaliser un test, il faut disposer d'un oracle.

Dans notre cas, cela signifie disposer d'un moyen de calculer la sortie qu'une implémentation correcte d'un modèle doit produire. Concrètement, cet "oracle" est une implémentation de référence. 

Cette implémentation de référence n'a pas à être efficace. Par contre, elle doit être parfaitement traçable vers la spécification (par ex. la spécification des opérateurs qu'elle met en oeuvre). 

Elle doit couvrir l'ensemble de la sémantique d'un modèle SONNX, ce qui comprend le graphe et les opérateurs mis en oeuvre par celui-ci (les noeuds). 

#### Concernant les opérateurs 

 Considérons par ex. l'opérateur de convolution. Les étapes sont les suivantes : 
- spécification informelle de l'opérateur de convolution pour les différents types de données et d'attributs supportés par SONNX 
- spécification formelle (par ex. en Why3 ou en ACSL) 
- implémentation en C de l'opérateur 
- vérification de la correction de l'implémentation par rapport à sa spécification en ACSL 
- intégration de l'implémentation de référence dans AIDGE

#### Concernant le graphe

 Même démarche que pour les opérateurs. 

Il faut cependant choisir une manière d'ordonnancer l'appel des opérateurs. Ce peut être un générateur de code qui va produire la séquence d'appel aux opérateurs. 

Le code généré doit être suffisamment simple pour faciliter la vérification de la sa conformité avec le graphe décrit par le fichier ONNX. 

Notez qu'ici, je veux fournir les moyens de  vérifier que l'implémentation de référence produit une bonne implémentation d'UN modèle (par ex. en fournissant des informations de traça vers le modèle ONNX) . Idéalement, on devrait garantir que l'implémentation de référence produit une implémentation correcte quel que soit le modèle. Je pense que la sémantique d'un graphe est suffisamment simple pour qu'une preuve de l'implémentation soit faisable. C'est à nous de voir. Ce peut être fait en deux phases. C'est un sujet dont nous pourrons parler lors de la réunion SONNX sur l'usage des méthodes formelles. 

#### Actions

Faire l'exercice complet de la spécification jusqu'à l'implémentation de réference et son intégration dans AIDGE, pour quelques opérateurs et pour la structure d'exécution du graphe.
 Il me semble qu'ACETONE pourrait être une piste, mais j'avoue ne pas avoir bine compris commen s'articule / articulerait ACETONE et AIDGE.

Notez que l'on peut aussi partir de l'implémentation existante  et "remonter" vers la spec. 

## Banc d'évaluation 

Il pourrait être intéressant d'intégrer AIDGE dans notre banc afin de montre / démontrer que l'implémentation de référence produit les mêmes résultats sur différentes cibles matérielles. 


