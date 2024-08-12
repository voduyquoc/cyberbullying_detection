import boto3
import json
import base64
import logging
import pandas as pd
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

kinesis_client = boto3.client('kinesis')

CONSUME_STREAM_NAME = 'tweet_classification'

original_data = pd.read_csv('./data/data.csv')

def process_records(Records, data_dict):
    if len(Records) != 0:
        for i in range(0, len(Records)):
            result = json.loads(Records[i]['Data'].decode("utf-8"))
            print(result)
            tweet_id = result['prediction']['tweet_id']
            tweet_class = result['prediction']['classification']
            if tweet_id in data_dict['id']:
                index = data_dict['id'].index(tweet_id)
                data_dict['prediction'][index] = tweet_class
            else:
                data_dict['id'].append(tweet_id)
                data_dict['prediction'].append(tweet_class)
            print(f'Tweet id {tweet_id} is classified and recorded.')
    else:
        pass
    return data_dict

def main(stream_name):    
    try:
        kinesis_client = boto3.client('kinesis')
        response = kinesis_client.describe_stream(StreamName=stream_name)
        shard_id = response['StreamDescription']['Shards'][0]['ShardId']

        # Get the shard iterator.
        # ShardIteratorType=AT_SEQUENCE_NUMBER|AFTER_SEQUENCE_NUMBER|TRIM_HORIZON|LATEST|AT_TIMESTAMP
        response = kinesis_client.get_shard_iterator(
            StreamName=stream_name,
            ShardId=shard_id,
            ShardIteratorType='TRIM_HORIZON'
        )
        shard_iterator = response['ShardIterator']

        max_records = 20
        record_count = 0
        data_dict = {'id': [], 'prediction': []}

        while record_count < max_records:
            response = kinesis_client.get_records(
                ShardIterator=shard_iterator,
                Limit=20
            )
            shard_iterator = response['NextShardIterator']
            records = response['Records']
            if len(records) == 0:
                pass
            else:
                record_count = record_count + len(records)
                data_temp = process_records(records, data_dict)

        df = pd.DataFrame(data_temp)
        df['id'] = df['id'].astype(int)
        current_data = pd.merge(original_data, df, on='id', how='inner')
        current_data['prediction'] = current_data['prediction'].apply(lambda x: 1 if x == 'cyberbullying' else 0)
        current_data.to_csv('./data/current.csv', index=False)

    except ClientError as e:
        logger.exception("Couldn't get records from stream %s.", stream_name)
        raise


if __name__ == "__main__":
    main(CONSUME_STREAM_NAME)