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
      - Est ce possible de généraliser le type des tenseurs pour éviter de réecrire la spécification pour le type real.
  - graphe ONNX : graph (repo)
    - Problèmes rencontrés :
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
