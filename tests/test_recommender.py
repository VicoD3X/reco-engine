import numpy as np
import pandas as pd

from src.recommender import Recommender


def _sample_recommender() -> tuple[Recommender, pd.DataFrame]:
    embeddings = np.array(
        [
            [1.0, 0.0, 0.0],
            [0.9, 0.1, 0.0],
            [0.8, 0.2, 0.0],
            [0.0, 1.0, 0.0],
            [0.0, 0.0, 1.0],
            [0.5, 0.5, 0.0],
        ],
        dtype=np.float32,
    )
    clicks = pd.DataFrame(
        {
            "user_id": [1, 1, 2],
            "click_article_id": [0, 3, 4],
        }
    )
    return Recommender(X=embeddings, top_popular=[4, 5, 2, 1, 0]), clicks


def test_cold_start_uses_popularity_fallback():
    recommender, clicks = _sample_recommender()

    recommendations = recommender.recommend(user_id=999, clicks=clicks, k=3)

    assert recommendations == [4, 5, 2]


def test_recommendation_count_matches_k():
    recommender, clicks = _sample_recommender()

    recommendations = recommender.recommend(user_id=1, clicks=clicks, k=3)

    assert len(recommendations) == 3


def test_already_clicked_articles_are_excluded():
    recommender, clicks = _sample_recommender()

    recommendations = recommender.recommend(user_id=1, clicks=clicks, k=4)

    assert 0 not in recommendations
    assert 3 not in recommendations


def test_unknown_user_does_not_crash():
    recommender, clicks = _sample_recommender()

    recommendations = recommender.recommend(user_id=404, clicks=clicks, k=2)

    assert recommendations == [4, 5]
