# Data and artifacts

This folder contains a small demo subset used by the Streamlit interface and local checks.

## Versioned data

- `articles_metadata.csv`: article metadata used by the frontend to enrich recommendation outputs.
- `clicks_sample.csv`: click-history sample used for local validation and popularity baseline examples.

## Model artifacts

The production-style deployment loads model artifacts from Azure Blob Storage rather than relying on large local files committed to Git.

The Azure Function expects the following blobs:

- `articles_embeddings_pca50.joblib`
- `clicks_sample.csv`

To run the recommendation engine locally, generate or retrieve `articles_embeddings_pca50.joblib` and place it in this folder before launching `py -m src.run_local_test`.

## Why the full data is not committed

The original dataset and generated artifacts can be large. Keeping only a representative sample makes the repository easier to review, clone and run as a portfolio project while preserving the architecture used for deployment.
