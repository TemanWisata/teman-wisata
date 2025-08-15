from rectools.models.base import ModelBase
from rectools.dataset import Dataset
import mlflow
import pandas as pd


class MlflowRecommender:
    model: ModelBase | None = None
    @classmethod
    def load_recommender(cls, model_uri: str):
        """Load the recommender model from MLflow."""
        if cls.model is None:
            cls.model = mlflow.pyfunc.load_model(model_uri).unwrap_python_model().recsys_model
        return cls.model

    @classmethod
    def recommend(cls, model_input:list[int], dataset:Dataset, k=10, filter_viewed=True):
        """Get recommendations for a user."""
        if cls.model is None:
            raise ValueError("Model not loaded. Call load_recommender first.")
        return cls.model.recommend(model_input, dataset, k, filter_viewed)