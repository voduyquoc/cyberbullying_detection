
KINESIS_STREAM_INPUT=tweet_events
aws kinesis put-record \
    --stream-name ${KINESIS_STREAM_INPUT} \
    --partition-key 1 \
    --data '{ 
        "tweet": {
            "tweet_text": "In other words"
        }, 
        "tweet_id": 123
    }'

KINESIS_STREAM_INPUT=tweet_events
aws kinesis put-record \
    --stream-name ${KINESIS_STREAM_INPUT} \
    --partition-key 1 \
    --data "Hello, this is a test."

aws kinesis create-stream --stream-name mlops-stream --shard-count 1

aws kinesis describe-stream --stream-name mlops-stream

aws lambda create-event-source-mapping --function-name mlops-test \
--event-source  arn:aws:kinesis:eu-north-1:381492288364:stream/mlops-stream \
--batch-size 100 --starting-position LATEST

aws lambda list-event-source-mappings --function-name mlops-test \
--event-source arn:aws:kinesis:eu-north-1:381492288364:stream/mlops-stream

aws kinesis put-record --stream-name mlops-stream --partition-key 1 \
--data "Hello, this is a test." --cli-binary-format raw-in-base64-out

KINESIS_STREAM_INPUT=tweet_events  
aws kinesis put-record \
    --stream-name ${KINESIS_STREAM_INPUT} \
    --partition-key 1 \
    --data '{ 
        "tweet": {
            "tweet_text": "Love that the best response to the hotcakes they managed to film was a non-committal"
        }, 
        "tweet_id": 99
    }' \
    --cli-binary-format raw-in-base64-out


export PREDICTIONS_STREAM_NAME="tweet_predictions"
export S3_BUCKET_NAME="mlops-zoomcamp-quocvo"
export RUN_ID="02377ce8d5ec4fd9944b79ba3f345475"
export TEST_RUN="True"

python test.py


KINESIS_STREAM_OUTPUT='tweet_predictions'
SHARD='shardId-000000000000'

SHARD_ITERATOR=$(aws kinesis \
    get-shard-iterator \
        --shard-id ${SHARD} \
        --shard-iterator-type TRIM_HORIZON \
        --stream-name ${KINESIS_STREAM_OUTPUT} \
        --query 'ShardIterator' \
)

RESULT=$(aws kinesis get-records --shard-iterator $SHARD_ITERATOR)

echo ${RESULT} | jq -r '.Records[0].Data' | base64 --decode


docker build -t stream-model-tweet:v1 .

export AWS_ACCESS_KEY_ID=""
export AWS_SECRET_ACCESS_KEY=""
export AWS_DEFAULT_REGION=""


docker run -it --rm \
    -p 8080:8080 \
    -e PREDICTIONS_STREAM_NAME="tweet_predictions" \
    -e S3_BUCKET_NAME="mlops-zoomcamp-quocvo" \
    -e RUN_ID="fe0a57b41cf34581a9e613324c061ef6" \
    -e TEST_RUN="True" \
    -e AWS_ACCESS_KEY_ID="${AWS_ACCESS_KEY_ID}" \
    -e AWS_SECRET_ACCESS_KEY="${AWS_SECRET_ACCESS_KEY}" \
    -e AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION}" \
    stream-model-tweet:v1

python test_docker.py

aws ecr create-repository --repository-name tweet-model

aws ecr get-login-password --region <your-region> | docker login --username AWS --password-stdin <your-account-id>.dkr.ecr.<your-region>.amazonaws.com
aws ecr get-login-password --region eu-north-1 | docker login --username AWS --password-stdin 381492288364.dkr.ecr.eu-north-1.amazonaws.com

REMOTE_URI="381492288364.dkr.ecr.eu-north-1.amazonaws.com/tweet-model"
REMOTE_TAG="v1"
REMOTE_IMAGE=${REMOTE_URI}:${REMOTE_TAG}

LOCAL_IMAGE="stream-model-duration:v1"
docker tag ${LOCAL_IMAGE} ${REMOTE_IMAGE}
docker push ${REMOTE_IMAGE}

echo $REMOTE_IMAGE