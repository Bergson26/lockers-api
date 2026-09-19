# Décisions — pipeline CI

## Ce que j'ai mis dans le pipeline et pourquoi

Trois jobs qui tournent en parallèle : lint, tests, sécurité.

**Lint (ruff)** : c'est la vérification la plus rapide et la moins coûteuse. Elle détecte les erreurs de style et les mauvaises pratiques sans avoir à exécuter le code. En pratique, ruff a remonté un problème de type sur `os.getenv()` — la valeur par défaut était un entier au lieu d'une string. Le code fonctionnait quand même à l'exécution, mais c'était une incohérence réelle.

**Tests (pytest)** : la suite existait déjà, il suffisait de la brancher. Le CI a révélé deux problèmes : un `ModuleNotFoundError` parce que le path Python n'était pas configuré pour un environnement propre (corrigé avec `pytest.ini`), et un bug dans `occupancy_rate()` qui arrondissait à 1 décimale au lieu de 2. C'est exactement ce pour quoi on fait de la CI.

**Sécurité (bandit + pip-audit)** : bandit analyse le code à la recherche de patterns dangereux. Il a détecté `debug=True` hardcodé dans Flask — une faille critique si le code partait en production tel quel, car le debugger Werkzeug permet d'exécuter du code arbitraire depuis le navigateur. `pip-audit` vérifie les dépendances contre les CVE connus. Ces deux outils prennent 10 secondes à intégrer et peuvent éviter des incidents sérieux.

J'ai choisi de faire tourner les trois jobs en parallèle plutôt qu'en séquence pour gagner du temps. Un développeur qui attend un retour CI pendant 3 minutes n'attend pas — il passe à autre chose et perd le contexte.

---

## Ce que j'ai volontairement laissé de côté

**La couverture de tests (coverage)** : ajouter un rapport de couverture sans ajouter de tests n'aurait pas grand intérêt. La suite actuelle couvre la logique métier mais pas les routes HTTP. Mettre un seuil de 80% avec 3 tests existants aurait bloqué le pipeline sans apporter de valeur réelle.

**Un job de build ou de déploiement** : je ne connais pas l'environnement cible (conteneur Docker, serveur classique, PaaS). Mettre un déploiement fictif n'aurait servi à rien.

**Les notifications** : Slack ou email en cas d'échec CI sont utiles en équipe, mais ça demande une configuration côté organisation GitHub que je n'avais pas.

**Un linter sur les fichiers de configuration** : yaml, json. Utile mais pas prioritaire sur un projet de cette taille.

---

## Par quoi je continuerais avec une semaine

1. Ajouter des tests sur les routes Flask — actuellement `main.py` n'est pas du tout couvert. Un test qui simule un appel HTTP avec un mauvais token, un statut inconnu, un casier inexistant.
2. Mettre en place la couverture une fois les tests en place, avec un seuil minimum.
3. Documenter l'endpoint `/stats` — il y a une note dans le README qui dit "penser à documenter le endpoint /stats", c'est resté en suspens.
4. Configurer les branch protection rules sur GitHub pour que les conventions du fichier `CONVENTIONS.md` soient réellement appliquées.

---

## Ce qui m'a manqué pour faire l'exercice

Pas grand chose techniquement. J'aurais aimé savoir comment l'application est déployée en production pour adapter le pipeline en conséquence — un job de build Docker ou un déploiement automatique sur une branche donnée aurait eu plus de sens avec ce contexte.
