## Setup MLflow

Change directory to `training` folder
```bash
cd cyberbullying-detection/training
```

Run the following to start the mlflow tracking server
```bash
mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root=s3://mlops-zoomcamp-cyberbullying/
```

## Setup Prefect

Run `prefect` server
```bash
prefect server start
```

Start the prefect worker
```bash
prefect worker start --pool cyberbullying
```

Run the ML model training and model registration pipeline
```bash
prefect deployment run 'Train Model Pipeline/cyberbullying_flow'
```

Below is the screenshot of the Prefect Deployment:

