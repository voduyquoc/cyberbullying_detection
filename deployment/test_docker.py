import requests 

event = {
    "Records": [
        {
            "kinesis": {
                "kinesisSchemaVersion": "1.0",
                "partitionKey": "1",
                "sequenceNumber": "49654286953440519834313401350639454381039437097331589122",
                "data": "eyAKICAgICAgICAidHdlZXQiOiB7CiAgICAgICAgICAgICJ0d2VldF90ZXh0IjogIkhlbGxvLCB0aGlzIGlzIGEgdGVzdC4iCiAgICAgICAgfSwgCiAgICAgICAgInR3ZWV0X2lkIjogMTIzCiAgICB9",
                "approximateArrivalTimestamp": 1721999702.184
            },
            "eventSource": "aws:kinesis",
            "eventVersion": "1.0",
            "eventID": "shardId-000000000000:49654286953440519834313401350639454381039437097331589122",
            "eventName": "aws:kinesis:record",
            "invokeIdentityArn": "arn:aws:iam::381492288364:role/lambda-kinesis-role",
            "awsRegion": "eu-north-1",
            "eventSourceARN": "arn:aws:kinesis:eu-north-1:381492288364:stream/tweet_events"
        }
    ]
}

url = 'http://localhost:8080/2015-03-31/functions/function/invocations'
response = requests.post(url, json=event)
print(response.json())
