# cyberbullying_detection

A data pipeline with Terraform, MLflow, Prefect, Docker, AWS (EC2, Lambda, S3, Kinesis, ECR, IAM), Evidently AI, Grafana and much more!

## Description

### Problem

...

### Objective

....

### Dataset

.... 

### Tools & Technologies

- Cloud - [**Amazon Web Services**](https://aws.amazon.com/)
- Virtual machine - [**Amazon EC2**](https://aws.amazon.com/ec2/)
- Infrastructure as Code software - [**Terraform**](https://www.terraform.io)
- Containerization - [**Docker**](https://www.docker.com) and [**Docker Compose**](https://docs.docker.com/compose/)
- Orchestration - [**Prefect**](https://www.prefect.io/)
- Experiment tracking and model management - [**MLflow**](https://mlflow.org/)
- Model artifacts storage - [**Amazon S3**](https://aws.amazon.com/s3/)
- Streaming model deployment - [**AWS Lambda**](https://aws.amazon.com/lambda/) and [**Amazon Kinesis**](https://aws.amazon.com/kinesis/)
- Container storage - [**Amazon ECR**](https://aws.amazon.com/ecr/)
- Model monitoring - [**Evidently AI**](https://www.evidentlyai.com/) and [**Grafana**](https://grafana.com/)
- Language - [**Python**](https://www.python.org)

### Architecture

...

### Exploratory Data Analysis and Modeling
The exploratory data analysis and modeling is done in the `notebooks` directory. The exploratory data analysis is done in the [exploratory-data-analysis.ipynb](notebooks/exploratory-data-analysis.ipynb) notebook. The modeling is done in the [modeling.ipynb](notebooks/modeling.ipynb) notebook.

### Training Pipeline

...

### Experiment Tracking & Model Registry

...

### Streaming Deployment

...

### Model Monitoring

...

## Setup

**WARNING: You will be charged for all the infra setup. You try free trials or 12 months free tier on AWS.**
### Pre-requisites

If you already have an Amazon Web Services account, you can skip the pre-requisite steps.

- Amazon Web Services: [AWS Account and Access Setup](setup/1_aws.md)

### Get Going

- SSH into your Virtual Machine - [Setup](setup/2_ssh.md)
- Procure infrastructure on AWS with Terraform - [Setup](setup/3_terraform.md)
- Setup Prefect and MLflow on Virtual Machine to trigger the training pipeline - [Setup](setup/4_prefect_mlflow.md)
- Streaming deployment - [Setup](setup/5_streaming.md)
- Monitoring - [Setup](setup/6_monitoring.md)
- Testing, Code Formatting and Pre-commit hooks - [Setup](setup/7_best_practices.md)

### Further Improvement

- Include CI/CD

### Special Mentions
I'd like to thank the [DataTalks.Club](https://datatalks.club) for offering this Data Engineering course for completely free. All the things I learnt there, enabled me to come up with this project. If you want to develop skill on Machine Learning Operations (MLOps) technologies, please check out the [course](https://github.com/DataTalksClub/mlops-zoomcamp).