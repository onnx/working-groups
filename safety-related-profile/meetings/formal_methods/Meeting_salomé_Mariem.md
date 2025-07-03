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
  - créer un cas de test,
  - appeler la fonction à tester (`add`),
  - afficher le résultat pour validation.

---

## 2. Problématiques identifiées

### Limitation des types numériques en OCaml

- OCaml ne propose que le type `int`, lié à l'architecture.
- Il n'existe pas de prise en charge native pour des types comme `int32` ou `float32`, nécessaires à nos tests.

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

