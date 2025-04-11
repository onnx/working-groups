**Participants**
- Franck VEDRINE (CEA, développeur de l'outil Fluctuat)
- Mariem TURKI (IRT St-Ex)
- Jean SOUYRIS (Airbus)
- Eric JENN (IRT St-Ex)

**Objet :** 
- Présentation du groupe de travail SONNX à Franck
- Discussion ouverte, pistes

**Résumé de la discussion**

- On va s'intéresser en premier lieu aux réseaux utilisant 
  - des données entières (réseaux quantifiés),  par ex. int8 et 
  - des données `float` en 16, 32 et 64 dans la mesure où 
    - ces données respectent le standard IEEE
    - ce sont celles qui intéressent le domaine critique. 

- On peut faire une analogie entre nos travaux sur les opérateurs de graphes et les opérateurs SCADE. Les besoins sont assez proches. Les différences résident dans :
  - la quantité d'opérations réalisées (énorme dans le cas des réseaux de neurones)...
  - la difficulté à déterminer l'impact des erreurs de calcul sur la performance de la fonction (que est l'effet d'une erreur sur un opérateur sur la décision finale?...).
- Dans tous les cas (?) il semble difficile de spécifier des objectifs d'erreur (relative ou absolue) au niveau des opérateurs. 
  - Même dans des cas plus classiques, il est d'ailleurs assez rare que ces exigences soient spécifiées *a priori*, sauf dans certains cas particuliers.
	
- La démarche actuelle est plus "pragmatique" : elle consiste à déterminer l'erreur max que l'on peut garantir avec un effort donné (best effort). 
- Cette erreur devient la spécification dans le sens où elle est (ou peut être) prise en compte au niveau système pour réaliser les fonctions (par ex. des filtrages).

- Cette évaluation nécessite de prendre en compte 
	- l'erreur liée à la méthode
	- l'erreur liée à l'implémentation

- Actuellement, nous ne spécifions dans SONNX ni la méthode ni l'implémentation. Cette approche n'est donc pas applicable à ce niveau.

- Par contre, nous pouvons l'appliquer au niveau de l'implémentation de référence :
	- On peut donner une estimation de l'erreur sur cette implémentation
	- Attention : il est possible que cette erreur ne puisse être atteinte que sur une implémentation simple et que la précision se dégrade sur des implémentation plus complexes, optimisées...
	- Cela conduirait à spécifier des erreurs impossibles à tenir...
	- On pourrait proposer une estimation pour plusieurs implémentations : 	
		- une simple (notre "implémentation de référence" obtenue via Why3), facilement analysable (?) et potentiellement peu efficace 
		- et une plus complexe et plus efficace.
	- Dans tous les cas :
		- dans le domaine critique, les implémentation devraient rester relativement simples 
		- sinon, libre à l'applicant de développer sa propre implémentation et d'appliquer la méthode préconisée.
- Afin de traiter le maximum de cas (même ceux complexes ne pouvant donner lieu à une estimation formelle), l'évaluation pourrait être catégorisée en 
	- Bronze : évaluation d'erreur "incomplète"
	- Argent: interprétation abstraite (fluctuat)
	- Or : preuve axiomatique

- Nous pourrions aussi nous contenter de décrire la méthode d'obtention de l'erreur.
  - Cependant, dans la mesure du possible, on va chercher à donner les moyens d'estimer cette l'erreur, potentiellement sous la forme d'une expression analytique ou d'une programme de calcul lorsque l'erreur dépend des caractéristiques des tenseurs d'entrée (par ex. nombre de dimension et taille).  

- Dans certains cas d'usage, le domaine de certains paramètres d'entrée des opérateur peut être borné et connu (par ex. valeurs dans [-1,1]). Ce type d'information permettrait d'améliorer la précision des évaluations
	- Il faut voir dans quelles situations ces contraintes s'appliquent.

- Disposer d'une estimation de l'erreur est aussi un moyen 
	- de faciliter le déboguage un modèle dans la mesure ou ell epermet d'ident
	- de réaliser des analyses / diagnostics "post-mortem" en cas de défaillance.
	- d'avoir des information su rl'origine des erreurs en sortie
	
- Franck est intéressé par le sujet et accepte de rejoindre le groupe de travail.
- Lui transmettre  
	- [X] les invitations
	- [X] les liens vers les documents 
- [X] Lui donner accès au git.
 





