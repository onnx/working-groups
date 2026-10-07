# Compte rendu de réunion — Avancement sur le type `scalar` et génération du code C

**Date :** 24/07/2025  
**Participants :** Salomé, Mariem  
**Sujet :** Avancement sur le type `scalar` et génération du code C

---

## 1. Points discutés

Salomé a résumé ce qu'elle a fait pendant les deux dernières semaines. Elle a :

1. Vérifié que l’opération d’arrondi utilisée dans ONNXRuntime est la même que celle utilisée dans Why3, à savoir **RNE**.  
2. Cloné le type `scalar` générique pour définir les types `ScalarInt32` et `ScalarFloat32`, en utilisant les bibliothèques `mach.int.Int32` et `ieee_float.Float32`.  
3. Implémenté l’opérateur générique `add` prenant un type `t` en paramètre.  
4. Cloné l’opérateur générique `add` pour définir les modules `OpAdd_Float32` et `OpAdd_Int32`.  
5. Généré le code OCaml.  
6. Créé les fichiers de tests et testé le comportement de l’opérateur `add` avec `int32` et `float32`, dans les cas d’addition avec et sans débordement.  
7. Réussi à générer un code C à partir de l’implémentation naïve du type `scalar`, mais la génération est incomplète : seule la structure de données `scalar` est traduite en C. Des problèmes sont rencontrés lors de la traduction de l’opérateur `add`.

---

## 2. Problématiques identifiées

- Le test de l’opérateur `add` avec des `float32` en cas de débordement ne donne pas le même résultat que ONNX, car le type `Float32` n’existe pas dans OCaml (seul le type `float64` y est disponible).  
  **Solutions possibles :**
  - Définir `float32` en OCaml.
  - Générer du code C pour les tests.

- Certaines expressions en WhyML ne peuvent pas se traduire en C, comme : `match ... with`.  
- La structure utilisée pour définir `scalar` est un peu complexe ; elle pourrait être simplifiée afin de faciliter la génération du code C.  
  Une autre solution possible : ne générer en C que les types problématiques en OCaml (notamment `float32`), pour éviter de devoir traduire le type générique complet.

---

## 3. Actions à venir

- Enrichir le type `scalar` avec des opérations logiques et des preuves, car l’implémentation actuelle ne contient que des opérations fonctionnelles.  
- Optimiser la structure du type `scalar` générique traduite en C (à discuter avec l’équipe et Loïc).  
- Tenter de générer du code C à partir de l’implémentation **non naïve** du type `scalar`.  


---


# Compte rendu de réunion — Avancement sur le type `scalar` 

**Date :** 03/07/2025 
**Participants :** Salomé, Mariem  
**Sujet :** Avancement sur le type `scalar`

---

## 1. Points discutés

### Test de l'opérateur `add` (int32 et float32)

- Salomé a implémenté un test de l'opérateur `add` en utilisant la librairie `ieee_int32` de Why3.
- La création du **driver `type.drv`** a été complexe et a demandé un temps significatif.
- À l’avenir, **solliciter Loïc**, qui dispose de **drivers déjà implémentés** pouvant être réutilisés.

### Modifications des fichiers OCaml

- Les fichiers `tensor.ml` et `tensor.mli` ont été modifiés pour :
  - appeler la fonction à tester (`add`),
  - afficher le résultat pour validation.

### Création du fichier de test OCaml

- Les fichiers `test_add.ml` et `test_add.expected` ont été générés pour :
  - réaliser des cas simples de test des types `int32` ou `float32`,
  - en exploitant les fonctions des fichiers `tensor.ml` et `tensor.mli`.

---

## 2. Problématiques identifiées

### Limitation des types numériques en OCaml

- OCaml ne propose que les types `int`, lié à l'architecture, et `int32`.
- Il n'existe pas de prise en charge native pour des types comme `int8` ou `float32`, nécessaires à nos tests.

### Comportement de l’arrondi dans Why3 vs ONNX

- Why3 utilise un **arrondi RNE (Round to Nearest Even)** pour les opérations `float32`.
- Il est nécessaire de **vérifier si cet arrondi correspond** à celui défini dans ONNX.
- Il faudra **étudier le code source de l’opérateur `add` dans ONNX** pour :
  - identifier les **opérations à redéfinir** dans `scalar`,
  - et celles **importables directement** depuis Why3.

---

## 3. Actions à venir

- Vérifier le comportement d’arrondi dans ONNX (comparé à RNE de Why3).
- Déterminer quelles opérations seront :
  - redéfinies dans le type `scalar`,
  - ou importées depuis les bibliothèques Why3.
- Formaliser les éléments **spécifiés informellement par Franck** dans la **spécification du type `scalar`**.

