import boto3
import json
import base64
import logging
import pandas as pd
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

kinesis_client = boto3.client('kinesis')

CONSUME_STREAM_NAME = 'tweet_predictions'

current_data = pd.read_parquet('./data/data.parquet')

def process_records(Records):
    if len(Records) != 0:
        for i in range(0, len(Records)):
            result = json.loads(Records[i]['Data'].decode("utf-8"))
            tweet_id = result['prediction']['tweet_id']
            tweet_class = result['prediction']['classification']
    else:
        pass
    return tweet_id, tweet_class

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
            record_count = record_count + len(records)
            tweet_id, tweet_class = process_records(records)
            if tweet_id in data_dict['id']:
                index = data_dict['id'].index(tweet_id)
                data_dict['prediction'][index] = tweet_class
            else:
                data_dict['id'].append(tweet_id)
                data_dict['prediction'].append(tweet_class)
            print(f'Tweet id {tweet_id} is classified and recorded.')

        df = pd.DataFrame(data_dict)
        df.to_parquet('./data/current.parquet', index=False)

    except ClientError as e:
        logger.exception("Couldn't get records from stream %s.", stream_name)
        raise


if __name__ == "__main__":
    main()