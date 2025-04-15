import boto3
import json
import pytest
from moto import mock_dynamodb
import lambda_function  # Asegúrate de que tu archivo se llame lambda_function.py

@pytest.fixture
def setup_dynamodb():
    with mock_dynamodb():
        # Crear el recurso de DynamoDB en us-east-1
        dynamodb = boto3.resource("dynamodb", region_name="us-east-1")

        # Crear la tabla necesaria
        dynamodb.create_table(
            TableName="visitor-counter-table-sam",
            KeySchema=[
                {"AttributeName": "id", "KeyType": "HASH"}
            ],
            AttributeDefinitions=[
                {"AttributeName": "id", "AttributeType": "S"}
            ],
            BillingMode="PAY_PER_REQUEST"
        )

        yield

def test_lambda_handler(setup_dynamodb):
    # Simular evento de API Gateway
    event = {
        "httpMethod": "GET",
        "path": "/",
        "headers": {},
        "body": None
    }

    result = lambda_function.lambda_handler(event, None)
    body = json.loads(result["body"])

    assert result["statusCode"] == 200
    assert "message" in body
    assert "count" in body
