## MLflow & Prefect

DAG Flow -
  - We first load data which is obtained from Kaggle. 
  - We then transform data then vector it to train ML models. This data is split to training data and validation data
  - Logistic Regression, Naive Bayes and K-Nearest Neighbors are used to find the model which has the highest accuracy in validation data.
  - The model which has highest accuracy will be train on all data to be ready to use in production.
  - Then we pack the resulted vectorizer and model into a pipeline, register it in MLflow registry. All trained model artifacts are stored in AWS S3, identified by their `run_id`. 
  - Finally, we have a final model which is ready to be used in productions.

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

There are 2 options to run training pipeline.

Option 1: Run the prefect flow below
    ```bash
    python training.py
    ```

Option 2: Trigger Prefect flow

- Update the `repository` value in the `prefect.yaml` file to your repository.

- Start the prefect worker
    ```bash
    prefect worker start --pool cyberbullying
    ```

- Deploy the flow
    ```bash
    prefect deploy training.py:main_flow -n cyberbullying_flow -p cyberbullying
    ```

- Run the ML model training and model registration pipeline
    ```bash
    prefect deployment run 'Train Model Pipeline/cyberbullying_flow'
    ```

Below is the screenshot of the Prefect Deployment:

![prefect](images/prefect.png)

Below is the MLflow UI screenshot of the model training runs:

![mlflow](images/mlflow_1.png)

MLflow Model Registry:

![mlflow](images/mlflow_3.png)

Directory of model artifacts:

![mlflow](images/mlflow_2.png)

Model artifacts which are stored in S3 bucket:

![s3](images/s3_2.png)
