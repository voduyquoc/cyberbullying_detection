import re
import nltk
# nltk.download('punkt')
import mlflow
import pandas as pd
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from mlflow.entities import ViewType
from mlflow.tracking import MlflowClient
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from prefect import flow, task, get_run_logger


@task(name="Load Data", log_prints=True, retries=3, retry_delay_seconds=2)
def load_data(path):
    """
    Load Data from CSV File
    Load the data from the specified CSV file.

    Args:
        path (str): Path to the CSV file.

    Returns:
        pd.DataFrame: Loaded data as a DataFrame.
    """
    logger = get_run_logger()
    logger.info("Loading data from %s", path)
    df = pd.read_csv(path, nrows=20000)
    return df

# Compile regex patterns
stemmer = PorterStemmer()
stop_words = set(stopwords.words('english'))
html_pattern = re.compile('<.*?>')
non_alpha_pattern = re.compile('[^a-zA-Z]')
url_pattern = re.compile(r'http\S+|@\S+|#\S+')

def clean_text(text_series):
    """
    Clean Text Data
    Preprocess the text data by removing noise, special characters, URLs, etc.

    Args:
        pd.Series: Series containing text data to be cleaned.

    Returns:
        pd.Series: Cleaned text data.
    """
    # Remove HTML tags
    text_series = text_series.str.replace(html_pattern, '', regex=True)
    
    # Remove non-alphabetic characters and convert to lowercase
    text_series = text_series.str.replace(non_alpha_pattern, ' ', regex=True).str.lower()
    
    # Remove URLs, mentions, and hashtags from the text
    text_series = text_series.str.replace(url_pattern, '', regex=True)

    # Tokenize the text
    text_series = text_series.apply(nltk.word_tokenize)

    # Remove stopwords and stem the words
    text_series = text_series.apply(lambda words: [stemmer.stem(w) for w in words if w not in stop_words])

    # Join the words back into a string
    text_series = text_series.apply(lambda words: ' '.join(words))

    return text_series

@task(name="Prepare Data", log_prints=True)
def prepare_data(df):
    """
    Process Data
    Preprocess the text data by removing noise, special characters, URLs, etc.

    Args:
        pd.DataFrame: Series containing text data to be cleaned.

    Returns:
        X_train, y_train: data which ready to be use
    """
    logger = get_run_logger()
    logger.info("Cleaning text: Started")

    df['processed_text'] = clean_text(df['tweet_text'])
    X_train = df['processed_text']
    y_train = df['cyberbullying_type']

    logger.info("Cleaning text: Completed")

    return X_train, y_train

@task(name="Train LR Model", log_prints=True)
def train_lr_model(X, y):
    """
    Train Model
    Args:
        X_train, y_train: data which ready to be use

    Returns:
        machine learning model which is saved in defined directory
    """
    logger = get_run_logger()
    logger.info("Starting LR training process...")
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    with mlflow.start_run():
        
        # Create Pipeline
        pipeline = Pipeline(
            [
                ('vectorizer', CountVectorizer()),
                ('clf', LogisticRegression(max_iter = 1000)),
            ]
        )
        
        # Train the model
        pipeline.fit(X_train, y_train)
        test_acc = accuracy_score(y_test, pipeline.predict(X_test))

        # Log the model
        logger.info("Logging the model...")
        
        mlflow.set_tag("model", "Logistic Regression")

        mlflow.sklearn.log_model(pipeline, "model")
        mlflow.log_metric("test_accuracy", test_acc)

        logger.info("Completed LR training process...")

    return None

@task(name="Train NB Model", log_prints=True)
def train_nb_model(X, y):
    """
    Train Model
    Args:
        X_train, y_train: data which ready to be use

    Returns:
        machine learning model which is saved in defined directory
    """
    logger = get_run_logger()
    logger.info("Starting NB training process...")
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    with mlflow.start_run():
        
        # Create Pipeline
        pipeline = Pipeline(
            [
                ('vectorizer', CountVectorizer()),
                ('clf', MultinomialNB()),
            ]
        )
        
        # Train the model
        pipeline.fit(X_train, y_train)
        test_acc = accuracy_score(y_test, pipeline.predict(X_test))

        # Log the model
        logger.info("Logging the model...")
        
        mlflow.set_tag("model", "Naive Bayes")

        mlflow.sklearn.log_model(pipeline, "model")
        mlflow.log_metric("test_accuracy", test_acc)

        logger.info("Completed NB training process...")

    return None

@task(name="Register Best Model", log_prints=True)
def register_best_model(client, EXPERIMENT_NAME):

    logger = get_run_logger()
    logger.info("Select the model with the highest test accuracy...")

    experiment = client.get_experiment_by_name(EXPERIMENT_NAME)
    best_run = client.search_runs(
        experiment_ids=experiment.experiment_id,
        run_view_type=ViewType.ACTIVE_ONLY,
        max_results=1,
        order_by=["metrics.test_accuracy DESC"])[0]
    best_run_id = best_run.info.run_id

    # Register the best model
    logger.info("Register the best model...")
    mlflow.register_model(
        model_uri=f"runs:/{best_run_id}/models",
        name='cyberbullying_clf')
    
    return None

@flow(name="Train Model Pipeline", log_prints=True)
def main_flow():
    """
    Train Model Flow
    Prefect flow that orchestrates the data loading, cleaning, and model training process.

    """
    logger = get_run_logger()
    logger.info("Starting flow...")

    # MLflow settings
    MLFLOW_TRACKING_URI = 'http://127.0.0.1:5000'
    EXPERIMENT_NAME = "Training Model"
    mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)
    mlflow.set_experiment(EXPERIMENT_NAME)
    client = MlflowClient()

    # Load the data
    df = load_data("../data/raw/cyberbullying_tweets.csv")

    # Clean the text
    X_train, y_train = prepare_data(df)

    # Train the model
    train_lr_model(X_train, y_train)
    train_nb_model(X_train, y_train)

    # Register best model
    register_best_model(client, EXPERIMENT_NAME)

    return None


if __name__ == "__main__":
    main_flow()
