# Conventions Git — lockers-api

L'équipe est de 4 personnes avec des pratiques différentes. L'idée n'est pas d'imposer 15 règles d'un coup, mais de poser ce qui évite les problèmes les plus fréquents : l'historique illisible, les conflits évitables, et le code qui part en prod sans relecture.

---

## Nommage des branches

Format : `type/description-courte`

Exemples :
- `feat/add-locker-delete`
- `fix/occupancy-rate-rounding`
- `ci/add-github-actions`

Types acceptés : `feat`, `fix`, `ci`, `docs`, `refactor`, `test`, `chore`

**Automatisable ?** Oui — GitHub permet de bloquer les branches qui ne correspondent pas à un pattern via les branch protection rules.

---

## Messages de commit

Format : `type: description courte en minuscules`

Exemples :
- `feat: add DELETE endpoint for lockers`
- `fix: round occupancy rate to 2 decimal places`
- `ci: add GitHub Actions pipeline`

La description doit dire ce que le commit fait, pas comment il le fait. Un message comme `fix` ou `wip` ne sert à rien dans 6 mois.

**Automatisable ?** Oui — avec commitlint + husky (hook git qui vérifie le format avant chaque commit). Demande une installation locale par chaque dev.

---

## Pull Requests

- Pas de push direct sur `main`, tout passe par une PR
- 1 reviewer minimum obligatoire avant de merger
- Le CI doit être vert avant le merge (lint + tests + sécurité)
- Le titre de la PR suit le même format que les commits

**Automatisable ?** En grande partie — les règles CI requise et reviewer minimum sont configurables dans GitHub (Settings → Branches → Branch protection rules). L'habitude d'ouvrir une PR plutôt que de push direct reste une règle d'équipe à respecter.

---

## Stratégie de merge

Squash merge uniquement.

Si une PR contient des commits de travail (`wip`, `test2`, `fix typo`), le squash les regroupe en un seul commit propre sur `main`. L'historique de la branche principale reste lisible et chaque ligne correspond à une fonctionnalité ou correction identifiable.

**Automatisable ?** Oui — dans les paramètres GitHub du repo, on peut désactiver le merge commit et le rebase et n'autoriser que le squash.

---

## Ce que je mettrais en priorité

Si on devait choisir par où commencer :

1. **Branch protection sur main** (CI obligatoire + 1 reviewer) — c'est automatique, ça bloque les mauvaises pratiques sans demander d'effort à l'équipe
2. **Nommage des branches** — simple à adopter, visible dans l'interface GitHub
3. **Messages de commit** — demande un peu plus de rigueur mais rend l'historique utile sur le long terme

---

## Marche à suivre : ouvrir une Pull Request

*(convention choisie pour l'explication détaillée — voir énoncé 2b)*

1. Crée ta branche depuis `main` : `git checkout -b feat/ma-fonctionnalite`
2. Travaille et commite avec le bon format : `git commit -m "feat: description courte"`
3. Pousse ta branche : `git push -u origin feat/ma-fonctionnalite`
4. Sur GitHub, clique sur "Compare & pull request"
5. Donne un titre qui suit le format des commits
6. Décris en quelques lignes ce que la PR fait et pourquoi
7. Assigne un reviewer dans le panneau à droite
8. Attends que le CI soit vert et que le reviewer valide
9. Merge en squash (bouton "Squash and merge")
10. Supprime la branche après le merge — elle a rempli son rôle
