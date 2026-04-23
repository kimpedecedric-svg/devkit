# Phase 1 - Découverte des outils

## GitHub CLI (gh)
- **Ce qu'il fait**: Gère les dépôts, les tickets (issues) et les pull requests depuis le terminal.
- **Chose surprenante**: On peut lister les dépôts très rapidement avec `gh repo list`.
- **Cas d'usage à tester** : Créer des branches et des PR sans ouvrir le navigateur.

## GitHub Copilot CLI (gh copilot)
- **Ce qu'il fait** : Suggère des commandes shell à partir du langage naturel.
- **Chose surprenante** : La fonction `explain` qui détaille des commandes complexes.
- **Cas d'usage à tester** : Trouver des commandes git difficiles à mémoriser.

## Gemini
-**Ce qu'il fait** : IA multi-modale pour l'analyse de code et la génération de doc.
-**Chose surprenante** : On peut lui envoyer un fichier entier pour analyse.
- **Cas d'usage à tester** : Faire une revue de code automatique sur mes scripts Python.

## Outils visuels (fzf, bat, delta)
-**fzf** : Un moteur de recherche floue pour retrouver des fichiers ou des commandes.
-**bat** : Remplace `cat` avec de la coloration syntaxique.
-**delta** : Rend l'affichage des `git diff` beaucoup plus lisible.

---
## Phase 2 - Architecture et Orchestration Python

Dans cette phase, j'ai structuré l'outil `devkit` pour orchestrer les commandes `gh`.

### Architecture du projet
- `src/devkit/utils/gh.py` : Module de base pour exécuter les commandes système et parser le JSON.
- `src/devkit/main.py` : Point d'entrée utilisant **Typer** pour les commandes et **Rich** pour l'interface.

### Commandes implémentées
- `devkit issues` : Récupère les tickets via `gh issue list --json` et les affiche dans un tableau formaté.
- `devkit prs` : Récupère les Pull Requests et permet une lecture rapide du statut du dépôt.

### Défis techniques rencontrés
- **Gestion du PYTHONPATH** : Nécessité d'exporter le chemin `src` pour que les imports Python fonctionnent.
- **Dépréciation de gh-copilot** : Observation de l'avertissement de GitHub, ce qui confirme l'importance de surveiller les dépendances.
- **Mode multi-commandes Typer** : Apprentissage du fonctionnement des groupes de commandes pour éviter que Typer ne traite le script comme une commande unique.

---
## Phase 3 - Intégration de l'IA (Gemini)

L'outil intègre désormais l'IA pour assister le développeur.

### Réalisations
- Création d'un module `src/devkit/utils/ai.py` utilisant le SDK `google-genai`.
- Implémentation d'un système de **fallback** et de **retry** pour gérer les limites de l'API (Erreurs 429 et 404).
- Commande `devkit suggest` pour interroger l'IA depuis le terminal.

### Analyse technique des limites
Durant les tests, j'ai rencontré des erreurs `429 RESOURCE_EXHAUSTED`. Cela démontre :
1. La bonne communication entre mon script et les serveurs de Google.
2. La nécessité de gérer les quotas d'API dans un outil de production.