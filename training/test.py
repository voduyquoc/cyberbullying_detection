import mlflow
from mlflow.entities import ViewType
from mlflow.tracking import MlflowClient

S3_BUCKET_NAME = "mlops-zoomcamp-quocvo"
MLFLOW_TRACKING_URI = 'http://127.0.0.1:5000'
EXPERIMENT_NAME = "Training Model"
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
mlflow.set_experiment(EXPERIMENT_NAME)
client = MlflowClient()

# Specify the model name and version
model_name = "cyberbullying_detection"

# Get all versions of the specified model
versions = client.search_model_versions(f"name='{model_name}'")

# Find the latest version
latest_version = max(versions, key=lambda v: int(v.version))

# Get the run ID of the latest version
run_id = latest_version.run_id
model_version = latest_version.version

print(f"The run ID for the latest version ({model_version}) of model {model_name} is: {run_id}")
