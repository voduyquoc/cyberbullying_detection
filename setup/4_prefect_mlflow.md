## MLflow & Prefect

Change directory to `training` folder
```bash
cd ~/cyberbullying_detection/training
```

Run the following to start the mlflow tracking server
```bash
mlflow server --backend-store-uri sqlite:///mlflow.db --default-artifact-root=s3://mlops-zoomcamp-cyberbullying/
```

Run `prefect` server
```bash
prefect server start
```

Deploy the flow
```bash
prefect deploy training.py:main_flow -n cyberbullying_flow -p cyberbullying
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

![prefect](images/prefect.png)

Below is the MLflow UI screenshot of the model training runs:

![mlflow](images/mlflow_1.png)

MLflow Model Registry:

![mlflow](images/mlflow_2.png)

![mlflow](images/mlflow_3.png)
