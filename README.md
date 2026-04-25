# Article Recommender - Azure Functions & Streamlit

End-to-end article recommendation MVP with content-based filtering, Azure Functions API and Streamlit frontend.

## Overview

This project delivers a deployable recommendation MVP for a content platform. It exposes an HTTP API that returns article recommendations for a given user and provides a Streamlit interface to test the recommender from a simple front end.

The repository focuses on the full product path of a machine learning feature: data preparation, recommendation logic, API deployment, frontend consumption and validation against a popularity baseline.

## Business objective

The goal is to help users discover relevant articles based on their reading history. For known users, the system generates personalized recommendations from previously clicked articles. For users without history, it falls back to globally popular articles so the service still returns useful results.

This makes the MVP usable in two important cases:

- Personalized recommendations for users with existing click history.
- Cold-start recommendations for unknown or new users.

## Architecture

```text
Streamlit frontend
        |
        v
Azure Functions HTTP API
        |
        v
Recommendation engine
        |
        v
Click history + article embeddings from Azure Blob Storage
```

The Streamlit app is intentionally lightweight: it calls the deployed API, displays the returned recommendations and compares them with a popularity baseline. The machine learning logic lives behind the Azure Functions API.

## Recommendation approach

The recommender uses a content-based filtering strategy:

- Article embeddings are reduced with PCA to keep inference lightweight.
- A user profile is computed from the average embedding of articles previously clicked by the user.
- Cosine similarity is used to rank candidate articles.
- Already clicked articles are filtered out of the final recommendations.
- A popularity fallback handles users with no available history.

The API response includes a `mode` field to distinguish personalized recommendations from cold-start fallback results.

## Repository structure

```text
.
|-- app/                 # Streamlit frontend
|-- azure_function/      # Azure Functions API
|-- data/                # Demo sample data and local artifact notes
|-- docs/                # Presentation support and validation material
|-- notebooks/           # Exploration notebook
|-- src/                 # Local recommendation module
|-- requirements.txt     # Streamlit app dependencies
|-- requirements-dev.txt # Development dependencies
`-- README.md
```

## Local setup

Create and activate a virtual environment:

```bash
py -m venv .venv
.venv\Scripts\activate
```

Install the Streamlit app dependencies:

```bash
pip install -r requirements.txt
```

Run the frontend:

```bash
streamlit run app/streamlit_app.py
```

For local tests of the recommendation engine, first place `articles_embeddings_pca50.joblib` in `data/`, then install the API/model dependencies:

```bash
pip install -r azure_function/requirements.txt
py -m src.run_local_test
```

## API usage

Demo endpoint:

```text
https://p10oc-recommender.azurewebsites.net/api/recommend
```

Example request:

```http
GET /api/recommend?user_id=0&k=5
```

Example response:

```json
{
  "user_id": 0,
  "k": 5,
  "mode": "content_based_pca50",
  "recommendations": [157519, 157944, 159495, 156690, 162857]
}
```

Cold-start example:

```http
GET /api/recommend?user_id=999999&k=5
```

Expected behavior: the API returns recommendations with `mode` set to `cold_start_popularity`.

## Streamlit demo

The Streamlit interface allows a user to:

- Select a user ID from the local demo sample.
- Choose the number of articles to recommend.
- Call the deployed Azure Functions API.
- Inspect the raw JSON response if needed.
- Compare personalized recommendations with a popularity baseline.

## Data and artifacts

The original dataset is not fully versioned in this repository. The repository keeps a demo sample so the frontend can display article metadata and the recommendation workflow remains understandable.

For deployment, model artifacts are loaded from Azure Blob Storage. The Azure Function expects these blobs:

- `articles_embeddings_pca50.joblib`
- `clicks_sample.csv`

For more details, see [data/README.md](data/README.md).

## Results and validation

Project validation confirmed that:

- The recommender returns the requested number of articles.
- Known users receive personalized content-based recommendations.
- Unknown users fall back to popular articles.
- The API response keeps a compact JSON format suitable for frontend consumption.

Example local outputs are documented in [docs/local_validation.txt](docs/local_validation.txt).

## Limitations

- The MVP uses a content-based approach only; it does not include collaborative filtering.
- The deployed API currently focuses on inference and does not retrain embeddings automatically.
- The local dataset is a demo sample, not the full production dataset.
- The Streamlit app is a demonstration frontend rather than a production UI.

## Next improvements

- Add automated tests for cold start, recommendation count and exclusion of already clicked articles.
- Hide raw exception details from API responses while keeping full errors in server logs.
- Add CI checks for linting and tests.
- Compare the content-based approach with collaborative filtering or hybrid methods.
- Add monitoring around API latency and recommendation coverage.

## Context

This project was initially built as part of the OpenClassrooms Data Scientist path. The repository has been cleaned and documented as a portfolio project focused on machine learning deployment.
