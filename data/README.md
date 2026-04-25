# Données et artefacts

Ce dossier contient les fichiers nécessaires à la démonstration locale du projet, ainsi que les conventions attendues pour les artefacts du moteur de recommandation.

## Fichiers inclus

- `articles_metadata.csv` : métadonnées des articles utilisées par l’interface Streamlit pour enrichir l’affichage des recommandations.
- `clicks_sample.csv` : échantillon d’historique de clics utilisé pour la démonstration locale et la baseline de popularité.
- `clicks/` : fichiers horaires issus du jeu de données de clics, conservés comme support d’exploration.

Le fichier `articles_metadata.csv` n’est pas vide. Il contient notamment les colonnes `article_id`, `category_id`, `created_at_ts`, `publisher_id` et `words_count`, qui permettent à Streamlit d’afficher des informations sur les articles recommandés.

## Fichiers non versionnés

Les artefacts complets du moteur de recommandation peuvent être volumineux et ne sont pas tous versionnés dans ce dépôt. Le moteur local attend en particulier le fichier suivant :

- `articles_embeddings_pca50.joblib`

Ce fichier doit contenir les embeddings d’articles réduits en 50 dimensions et être placé dans `data/` pour lancer `py -m src.run_local_test`.

## Déploiement Azure

La version déployée charge ses assets depuis Azure Blob Storage. L’Azure Function attend les blobs suivants :

- `articles_embeddings_pca50.joblib`
- `clicks_sample.csv`

La chaîne de connexion au storage est fournie à l’Azure Function via la variable d’environnement `RECO_STORAGE`.

## Lancement local

Pour lancer l’interface Streamlit, les fichiers versionnés suffisent à afficher les métadonnées et à consommer l’API déployée.

Pour lancer le moteur de recommandation localement, il faut aussi disposer de `data/articles_embeddings_pca50.joblib`. Sans cet artefact, le script local ne peut pas reconstruire les similarités entre articles.
