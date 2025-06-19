# 2025/06/20

## Agenda

[Schéma global](./image.png)

- (Mariem, Salomé, Eric et Jean) Présentation pour retour critique, de trois formalisations ainsi que des problèmes rencontrés
  - concat : concat (repo)
    - Problèmes rencontrés :
      - Complexité de la formalisation de l'opérateur : La nature "variadique" de l'opérateur combinée à la possibilité d'avoir des tenseurs de diverses dimensions
      - Introduction de clauses de spécification formelle (requires, ensures)
      - Appréhension des mécanismes de preuve
      - Exploitation efficace (?) des modules préexistants, comme Sequences et Tensors
  - conv 2D standard : repo (repo)
    - Problèmes rencontrés
      - Est ce qu'il y a des améliorations et/ou simplifications à proposer.
      - Comment gérer les erreurs de preuve (Exemple: la fonction conv2d_output_value)?
      - Est-il possible de généraliser le type des tenseurs pour éviter de réecrire la spécification pour le type real.
  - graphe ONNX : [graph](../../documents/profile_formal/onnxgraph.mlw) (repo)
    - Problèmes rencontrés : (voir [ici](#formalisation-du-graphe) en fin de ce document
- (Loïc) Preuves de l'existant
  - Obligations de preuve générées par l'outil
  - Propriétés utilisateurs
  - Processus de preuve
- (Mariem, Salomé, Eric et Jean) Besoin de spécification de type "relationnel" (voir schéma ci-dessus) en plus de la spécification fonctionnelle
  - Utile si la fonctionnelle n'est pas une redite de la relationnelle.
    -  Exemples :
      - Utile pour concat
      - Inutile pour where (l'opérateur traité lors de la première session).
- (Loïc) Processus de preuve spec fonctionnelle vs spec relationnelle
- Synthèse méthodologique
- Conclusion


### Formalisation du graphe

Voir le code [WhyML](../../documents/profile_formal/onnxgraph.mlw).

#### Q1: Choix de modélisation / implémentation

Pour implémenter la fonction qui associe une valeur à un tenseur, j'utilise une liste de (clé, valeur). Est-ce un bon choix? 

#### Q2 : Bibliothèques d'implémentation

Existe-t-il un "catalogue" d'implémentation des types de la bibliothèque standard?  Par exemple, une implémentation de Map sur la base des listes?

#### Q3 : Documentation et apprentissage

Existe-t-il une liste de "bons exemples" dont nous pourrions nous inspirer?

#### Q4: Démonstration simple qui n'aboutit pas...

Soit le petit exemple suivant :
``` whyml
let rec fold_left (f: 'acc -> 'a -> 'acc) (acc: 'acc) (l: list 'a) : 'acc
  variant { l }
= match l with
  | Nil -> acc
  | Cons x xs -> fold_left f (f acc x) xs
  end

predicate all_true (l: list bool)  = 
    forall b: bool. mem b l -> b = true

lemma and_true_true:
    forall a: bool, b: bool.  Bool.andb a b -> a /\  b
    
lemma  fold_left_and_equiv_all_true:
  forall l: list bool.
    fold_left Bool.andb true l = true <-> all_true l
```

Quelle approche préconiserais-tu pour spécifier la fonction "fold_left" ?

#### Q5 : Approche de preuve
Lorsqu'une preuve n'aboutit pas, il est difficle (pour un novice) de savoir comment procéder pour 
- déterminer s'il s'agit d'une incapacité du prouveur à réaliser la preuve ou une réelle erreur de spécification / implémentation
- corriger l'erreur (de spécification ou d'implémentation)...
Quelle démarche doit-on suivre pour traiter une preuve qui n'aboutit pas?

#### Q6 : Approche pour la preuve
Existe--il des constructions à éviter pour faciliter la preuve (et, réciproquement), existe-t-il des constructions à éviter (antipatterns?

#### Q7 : Lien entre spécification et implémentation
Je souhaite spécifier les fonctions en utilisant les constructions les plus abstraites possibles. Par exemple, je défini l'état d'un graphe comme une application d'un ensemble de tenseurs vers un ensemble de valeurs.

La déclaration est la suivante :
```
type graph_state = Map.map tensor (option value)
```
Je voudrais donc que ma spécification du comportement du graphe fasse référence à ce type abstrait. En pratique, la Map.map est implémentée au moyen d'une liste de (tenseur, valeur) :
```
type fmap = list (tensor,  option  value)
```
Je spécifie deux fonctions sur le type fmap: get et set.
- `fget_logic`
- `fset_logic`

J'implémente ces 2 fonctions (`fget` et `get`). 

Je démontre que 
- `fget` implémente bien `fget_logic` 
- `fset` implémente bien `fset_logic`  

Dans ce cas, il n'y a pas de différence entre l'implémentation et la spécification.

Maintenant, je souhaite établir le lien entre mon implémentation et la `Map` abstraite.

J'introduis deux lemmes montrer que les deux fonctions `fget` (resp. `fset`) et `Map.get` (resp. `Map.set`) retournent toujours les mêmes valeurs.

Est-ce la bonne approche?

#### Q8: Problème de preuve

Voir les lemmes `get_set_eq` et `get_set_neq` dans le  code [WhyML](../../documents/profile_formal/onnxgraph.mlw).







