# pylint: disable=duplicate-code

import os
import json
from pprint import pprint

import boto3
from deepdiff import DeepDiff

kinesis_endpoint = os.getenv('KINESIS_ENDPOINT_URL', "http://localhost:4566")
kinesis_client = boto3.client('kinesis', endpoint_url=kinesis_endpoint)

stream_name = os.getenv('PREDICTIONS_STREAM_NAME', 'tweet_classification')
shard_id = 'shardId-000000000000'


shard_iterator_response = kinesis_client.get_shard_iterator(
    StreamName=stream_name,
    ShardId=shard_id,
    ShardIteratorType='TRIM_HORIZON',
)

shard_iterator_id = shard_iterator_response['ShardIterator']


records_response = kinesis_client.get_records(
    ShardIterator=shard_iterator_id,
    Limit=1,
)


records = records_response['Records']
pprint(records)


assert len(records) == 1


actual_record = json.loads(records[0]['Data'])
pprint(actual_record)

expected_record = {
    'model': 'tweet_detection_model',
    'version': 'Test123',
    'prediction': {'tweet_id': 123, 'classification': 'not_cyberbullying'},
}

diff = DeepDiff(actual_record, expected_record, significant_digits=1)
print(f'diff={diff}')

assert 'values_changed' not in diff
assert 'type_changes' not in diff


print('all good')
