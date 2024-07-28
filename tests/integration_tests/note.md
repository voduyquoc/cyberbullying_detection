aws s3 cp --recursive s3://mlops-zoomcamp-cyberbullying/1/ff9ebbf78c044409acdf31730c1b9142/artifacts/model model

docker run -it --rm \
    -p 8080:8080 \
    -e PREDICTIONS_STREAM_NAME="tweet_classification" \
    -e RUN_ID="Test123" \
    -e MODEL_LOCATION="/app/model" \
    -e TEST_RUN="True" \
    -e AWS_DEFAULT_REGION="eu-north-1" \
    -v $(pwd)/model:/app/model \
    stream-model-cyberbullying-detection:v1

chmod +x run.sh

pipenv run pytest tests/
