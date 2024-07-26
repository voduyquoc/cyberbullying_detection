import json
import re
import base64
import boto3
import os
import mlflow

kinesis_client = boto3.client('kinesis')

PREDICTIONS_STREAM_NAME = os.getenv('PREDICTIONS_STREAM_NAME', 'tweet_predictions')

RUN_ID = os.getenv('RUN_ID')
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')

logged_model = f's3://{S3_BUCKET_NAME}/1/{RUN_ID}/artifacts/model'
model = mlflow.pyfunc.load_model(logged_model)


TEST_RUN = os.getenv('TEST_RUN', 'False') == 'True'



def clean_text(text):
    # Remove HTML tags
    text = re.sub('<.*?>', '', text)
    
    # Remove non-alphabetic characters and convert to lowercase
    text = re.sub('[^a-zA-Z]', ' ', text).lower()
    
    # Remove URLs, mentions, and hashtags from the text
    text = re.sub(r'http\S+', '', text)
    text = re.sub(r'@\S+', '', text)
    text = re.sub(r'#\S+', '', text)
    
    return text

def prepare_features(tweet):
    features = {}
    features['tweet_text'] = clean_text(tweet['tweet_text'])
    return features

def predict(text):
    pred = model.predict(text)
    return pred[0]

def lambda_handler(event, context):
    # print(json.dumps(event))
    
    predictions_events = []
    
    for record in event['Records']:
        encoded_data = record['kinesis']['data']
        decoded_data = base64.b64decode(encoded_data).decode('utf-8')
        tweet_event = json.loads(decoded_data)

        # print(tweet_event)
        tweet = tweet_event['tweet']
        print(tweet)
        print(type(tweet))
        tweet_id = tweet_event['tweet_id']
    
        features = prepare_features(tweet)
        # print(features)
        prediction = predict(features)
    
        prediction_event = {
            'model': 'tweet_detection_model',
            'version': '1',
            'prediction': {
                'tweet_id': tweet_id,
                'classification': prediction   
            }
        }
        
        if not TEST_RUN:
            kinesis_client.put_record(
                StreamName=PREDICTIONS_STREAM_NAME,
                Data=json.dumps(prediction_event),
                PartitionKey=str(tweet_id)
            )
        
        predictions_events.append(prediction_event)


    return {'predictions': predictions_events}
