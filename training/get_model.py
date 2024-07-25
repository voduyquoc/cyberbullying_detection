import mlflow
from mlflow.tracking import MlflowClient

# Initialize the MLflow client
MLFLOW_TRACKING_URI = 'http://127.0.0.1:5000'
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
client = MlflowClient()

# Specify the model name and version
model_name = "cyberbullying_clf"
model_version = 1  # or use the latest version

# Get the model version details
model_version_details = client.get_model_version(name=model_name, version=model_version)

# Extract the run ID
run_id = model_version_details.run_id

print(f"The run ID for model {model_name} version {model_version} is: {run_id}")
