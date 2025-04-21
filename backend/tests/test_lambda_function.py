import json
import boto3
import pytest
from moto import mock_dynamodb

from backend import lambda_function
@pytest.fixture
def setup_dynamodb():
    with mock_dynamodb():
        # Crear recursoss simulado de DynamoDB
        dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
        # Crear tabla que tu función Lambda necesita
        table = dynamodb.create_table(
            TableName="visitor-counter-table-sam",
            KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
            BillingMode="PAY_PER_REQUEST"
        )
        table.wait_until_exists()
        yield  # Se ejecuta la pruebas después de esta línea

def test_lambda_handler(setup_dynamodb):
    event = {
        "httpMethod": "GET",
        "path": "/",
        "headers": {},
        "body": None
    }

    result = lambda_function.lambda_handler(event, None)
    print("RESULT:", result)

    assert result["statusCode"] == 200
    body = json.loads(result["body"])
    assert "count" in body
    assert isinstance(body["count"], int)
