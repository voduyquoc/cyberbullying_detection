import boto3
import json
import base64
import pandas as pd


def produce(df, num_record, kinesis_client, produce_stream_name, partition_key):
    data = df.head(num_record)
    for i in range(num_record):
        record = data.iloc[i]
        tweet_id = record['id']
        tweet_text = record['tweet_text']
        send_data = {
            "tweet": {
                "tweet_text": tweet_text
            },
            "tweet_id": str(tweet_id)
        }

        data_bytes = json.dumps(send_data).encode('utf-8')

        kinesis_client.put_record(
            StreamName=produce_stream_name,
            Data=data_bytes,
            PartitionKey=partition_key
        )

        print(f'Record index {i} is sent.')

    return None

if __name__ == "__main__":

    kinesis_client = boto3.client('kinesis')

    PRODUCE_STREAM_NAME = 'tweet_events'
    PARTITION_KEY = '1'

    df = pd.read_csv('./data/data.csv')

    NUM_RECORD = 20

    produce(df, NUM_RECORD, kinesis_client, PRODUCE_STREAM_NAME, PARTITION_KEY)