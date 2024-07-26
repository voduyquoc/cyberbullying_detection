import boto3
import base64
import time
import binascii

KINESIS_STREAM_OUTPUT = 'tweet_predictions'
SHARD = 'shardId-000000000000'

def get_shard_iterator(client, stream_name, shard_id):
    """Get the shard iterator for the given shard ID."""
    response = client.get_shard_iterator(
        StreamName=stream_name,
        ShardId=shard_id,
        ShardIteratorType='TRIM_HORIZON'
    )
    return response['ShardIterator']

def get_records(client, shard_iterator):
    """Get records from the Kinesis stream using the shard iterator."""
    response = client.get_records(
        ShardIterator=shard_iterator
    )
    return response

def decode_base64(data):
    """Decode base64 encoded data and handle decoding errors."""
    try:
        return base64.b64decode(data).decode('utf-8')
    except (binascii.Error, UnicodeDecodeError) as e:
        print(f"Base64 decode error: {e}")
        return None

def main():
    # Initialize the Kinesis client
    client = boto3.client('kinesis')

    # Get the initial shard iterator
    shard_iterator = get_shard_iterator(client, KINESIS_STREAM_OUTPUT, SHARD)

    while True:
        # Get records from the Kinesis stream
        result = get_records(client, shard_iterator)

        # Process records if any
        if 'Records' in result and result['Records']:
            for record in result['Records']:
                record_data = decode_base64(record['Data'])
                if record_data:
                    print(f"Record Data: {record_data}")
                else:
                    print("Failed to decode record data.")
        else:
            print("No records found.")

        # Update the shard iterator to the next shard iterator
        shard_iterator = result.get('NextShardIterator')

        # Check for MillisBehindLatest to know if we have processed all available records
        millis_behind_latest = result.get('MillisBehindLatest', 0)
        if millis_behind_latest == 0:
            print("Reached the end of the stream.")
            break

        # Optional: Sleep for a short period to avoid overwhelming the API
        time.sleep(1)

    print("Successfully processed all records.")

if __name__ == "__main__":
    main()
