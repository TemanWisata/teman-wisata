from app.core.config import CONFIG
import os
import mlflow
import pandas as pd
import numpy as np
from pathlib import Path
import glob
from rectools.dataset import Dataset


from app.core.utils import Utils

os.environ["MLFLOW_TRACKING_URI"] = CONFIG.mlflow.tracking_uri
os.environ["AWS_ACCESS_KEY_ID"] = CONFIG.aws.access_key_id
os.environ["AWS_SECRET_ACCESS_KEY"] = CONFIG.aws.secret_access_key
os.environ["MLFLOW_S3_ENDPOINT_URL"] = "https://minio.teman-wisata.fun"
os.environ["MLFLOW_DISABLE_ENV_CREATION"] = "true"


mlflow.set_tracking_uri(CONFIG.mlflow.tracking_uri)
print("MLflow Model URI:", CONFIG.mlflow.model_uri)
print("MLflow Tracking URI:", CONFIG.mlflow.tracking_uri)
# Ensure the MLflow tracking URI is set


ROOT_PATH = Utils.get_root_path()
DATASET_PATH = str(ROOT_PATH.joinpath("datasets/*/*/*/*/*"))
datasets = list(map(lambda x: Path(x), glob.glob(DATASET_PATH)))

print(f"Datasets:{datasets}")

print("Preparing data...")
# Data Preparation
df = {data_path.stem: pd.read_csv(data_path) for data_path in datasets}
print(df.keys())

ratings_df = df["tourism_rating"]
ratings_df.columns = ["user_id", "item_id", "weight"]


# Define timestamp range (e.g., Jan 1, 2010 to Jan 1, 2020)
start_ts = pd.Timestamp("2010-01-01").timestamp()
end_ts = pd.Timestamp("2020-01-01").timestamp()

# Generate random timestamps
ratings_df["datetime"] = np.random.randint(
    start_ts, end_ts, size=len(ratings_df)
).astype(int)

print("Data preparation complete.")

print("Loading MLFlow model...")
# MLFlow model loading
model_uri = CONFIG.mlflow.model_uri
model = mlflow.pyfunc.load_model(model_uri=model_uri)
print("Model loaded successfully.")

print("Make recommendations...")
# Make recommendation
test_user = 20
# recos = model.recsys_model.recommend(data=[20],params={"dataset":ratings_df, "k":10, "filter_viewed": True})  # type: ignore
recos = model.unwrap_python_model().recsys_model.recommend(users=[test_user], dataset=Dataset.construct(interactions_df=ratings_df), k=10, filter_viewed=True)  # type: ignore
print(recos.head())