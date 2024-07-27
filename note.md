pipenv install scikit-learn mlflow prefect boto3 nltk

pipenv shell

mlflow server  --backend-store-uri sqlite:///mlflow.db --default-artifact-root=s3://mlops-zoomcamp-cyberbullying/

prefect server start

python training.py

prefect init --recipe local /prefect init --recipe git

prefect work-pool create cyberbullying --type process

prefect deploy training.py:main_flow -n cyberbullying_flow -p cyberbullying

prefect worker start --pool cyberbullying

prefect deployment run 'Train Model Pipeline/cyberbullying_flow'