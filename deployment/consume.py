import boto3
import json
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

def process_records(Records):
    if len(Records) != 0:
        for i in range(0, len(Records)):
            result = json.loads(Records[i]['Data'].decode("utf-8"))
            tweet_id = result['prediction']['tweet_id']
            tweet_class = result['prediction']['classification']
            print(f'Result: tweet_id: {tweet_id}, class: {tweet_class}.')
    else:
        pass
    return None


def main():
    stream_name = 'tweet_predictions'
    
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

        max_records = 8
        record_count = 0

        while record_count < max_records:
            response = kinesis_client.get_records(
                ShardIterator=shard_iterator,
                Limit=10
            )
            shard_iterator = response['NextShardIterator']
            records = response['Records']
            record_count += len(records)
            process_records(records)

    except ClientError as e:
        logger.exception("Couldn't get records from stream %s.", stream_name)
        raise


if __name__ == "__main__":
    main()