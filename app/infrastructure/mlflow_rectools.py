"""Mlflow Rectools integration for model management and tracking."""

import mlflow
import pandas as pd
from rectools.dataset import Dataset  # type: ignore  # noqa: PGH003
from rectools.models.base import ModelBase  # type: ignore  # noqa: PGH003


class MlflowRecommender:
    """Class to manage MLflow-based recommender models."""

    model: ModelBase | None = None

    @classmethod
    def load_recommender(cls, model_uri: str) -> ModelBase:
        """Load the recommender model from MLflow."""
        if cls.model is None:
            cls.model = mlflow.pyfunc.load_model(model_uri).unwrap_python_model().recsys_model
        return cls.model  # type: ignore  # noqa: PGH003

    @classmethod
    def recommend(cls, model_input: list[int], dataset: Dataset, k: int = 10, filter_viewed: bool = True) -> pd.DataFrame | Dataset:  # noqa: FBT001, FBT002
        """Get recommendations for a user.

        :param model_input: List of user IDs to get recommendations for.
        :param dataset: Dataset containing user-item interactions.
        :param k: Number of recommendations to return.
        :param filter_viewed: Whether to filter out items already viewed by the user.
        :return: DataFrame with recommendations.
        """
        if cls.model is None:
            msg = "Model not loaded. Call load_recommender first."
            raise ValueError(msg)
        return cls.model.recommend(model_input, dataset, k, filter_viewed)
