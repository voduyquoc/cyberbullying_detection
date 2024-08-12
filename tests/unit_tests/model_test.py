from pathlib import Path

import sys

sys.path.append(str(Path(__file__).resolve().parents[2]))
sys.path.append(str(Path(__file__).resolve().parents[2]) + '/deployment')

from deployment import model


def read_text(file):
    test_directory = Path(__file__).parent

    with open(test_directory / file, 'rt', encoding='utf-8') as f_in:
        return f_in.read().strip()


def test_base64_decode():
    base64_input = read_text('data.b64')

    actual_result = model.base64_decode(base64_input)
    expected_result = { 
        "tweet": {
            "tweet_text": "Hello, this is a test."
        }, 
        "tweet_id": 123
    }

    assert actual_result == expected_result


def test_prepare_features():
    model_service = model.ModelService(None)

    tweet = {
        "tweet_text": "Hello, this is a test."
    }

    actual_features = model_service.prepare_features(tweet)

    expected_features = {
        'tweet_text': 'hello  this is a test '
    }

    assert actual_features == expected_features


class ModelMock:
    def __init__(self, value):
        self.value = value

    def predict(self, X):
        n = len(X)
        return [self.value] * n


def test_predict():
    model_mock = ModelMock(10.0)
    model_service = model.ModelService(model_mock)

    features = {
        'tweet_text': 'hello  this is a test '
    }

    actual_prediction = model_service.predict(features)
    expected_prediction = 10.0

    assert actual_prediction == expected_prediction


def test_lambda_handler():
    model_mock = ModelMock(10.0)
    model_version = 'Test123'
    model_service = model.ModelService(model_mock, model_version)

    base64_input = read_text('data.b64')

    event = {
        "Records": [
            {
                "kinesis": {
                    "data": base64_input,
                },
            }
        ]
    }

    actual_predictions = model_service.lambda_handler(event)
    expected_predictions = {
        'predictions': [
            {
                'model': 'tweet_detection_model',
                'version': model_version,
                'prediction': {
                    'tweet_id': 123,
                    'classification': 10.0   
                },
            }
        ]
    }

    assert actual_predictions == expected_predictions