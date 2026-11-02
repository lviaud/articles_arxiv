# Articles arXiv

Collection de résumés français. Chaque page d'article affiche son titre et le résumé, sans autres métadonnées visibles.

## Contenu

- `articles/` : résumés Markdown ; le nom du fichier définit l'adresse de la page.
- `build.py` : génération du site avec Python 3.12, sans dépendance externe.
- `dist/` : pages produites, ignorées par Git.

Le résumé initial comporte 50 lignes de contenu, regroupées en dix paragraphes. Le nombre de lignes affichées varie avec la largeur de l'écran.

## Publication

Dans les réglages du dépôt `articles_arxiv`, ouvrir **Settings → Pages**, puis choisir **GitHub Actions** comme source. Ne pas configurer les modèles Jekyll ou Static HTML : le workflow est inclus.

La fusion de la proposition dans `main` déclenche la publication. Si la source Pages a été choisie après la fusion, relancer le workflow **Articles arXiv** depuis l'onglet **Actions**.

Adresse prévue après déploiement réussi : `https://lviaud.github.io/articles_arxiv/`.

## Génération locale

```sh
python build.py
python -m http.server 8000 --directory dist
```

## Évolution

Pour ajouter un résumé, créer un fichier `articles/nom-de-l-article.md`, avec le titre en première ligne, puis le texte réparti en paragraphes. Les pages et le catalogue sont générés automatiquement.

Le fichier public `articles.json` contient uniquement les titres, identifiants de page, liens relatifs et paragraphes. Il fournit un format simple pour un futur raccordement à une application ; aucun raccordement n'est réalisé ici.
