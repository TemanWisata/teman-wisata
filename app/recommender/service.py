"""Service for handling recommendations."""

import pandas as pd
from rectools.dataset import Dataset  # type: ignore  # noqa: PGH003

from app.infrastructure import MlflowRecommender


class RecommenderService:
    """Service for handling recommendations."""

    @classmethod
    def get_df_user_ratings(cls, dataframe: pd.DataFrame) -> Dataset:
        """Get user ratings DataFrame."""
        return Dataset.construct(interactions_df=dataframe)

    @classmethod
    def recommend(cls, user_id: list[int], dataset: Dataset, k: int = 10, filter_viewed: bool = True) -> pd.DataFrame | Dataset:  # noqa: FBT001, FBT002
        """Recommend places for a user.

        :param user_id: List of user IDs to recommend for.
        :param dataset: Dataset containing user-item interactions.
        :param k: Number of recommendations to return.
        :param filter_viewed: Whether to filter out items already viewed by the user.
        :return: DataFrame or Dataset containing recommendations.
        """
        return MlflowRecommender.recommend(model_input=user_id, dataset=dataset, k=k, filter_viewed=filter_viewed)
