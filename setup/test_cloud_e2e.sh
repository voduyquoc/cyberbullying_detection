export KINESIS_STREAM_INPUT="tweet_events"
export KINESIS_STREAM_OUTPUT="tweet_classification"

aws kinesis put-record  \
        --stream-name ${KINESIS_STREAM_INPUT}   \
        --partition-key 1  --cli-binary-format raw-in-base64-out  \
        --data '{ 
        "tweet": {
            "tweet_text": "Hello, this is a test."
        }, 
        "tweet_id": 123}' 

#SHARD_ITERATOR=$(aws kinesis get-shard-iterator --shard-id ${SHARD_ID} --shard-iterator-type TRIM_HORIZON --stream-name ${KINESIS_STREAM_OUTPUT} --query 'ShardIterator')

#aws kinesis get-records --shard-iterator $SHARD_ITERATOR
