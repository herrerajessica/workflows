import json
import boto3
import pytest
from moto import mock_dynamodb
from lambda_function import lambda_handler

@pytest.fixture
def setup_dynamodb():
      with mock_dynamodb():
        dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
        table = dynamodb.create_table(
            TableName="visitor-counter-table-sam",
            KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
            ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1}
        )
        table.put_item(Item={"id": "visitor_count", "visits": 0})
        yield table

def test_lambda_handler_get(setup_dynamodb):
    """Prueba que el contador de visitas se incrementa correctamente"""
    event = {"httpMethod": "GET"}
    response = lambda_handler(event, None)
    print("Lambda response:", response)  # Ver la respuesta en los logs

    body = json.loads(response["body"])

    assert response["statusCode"] == 200, f"Error en Lambda: {response}"  # Mostrar error si falla
    assert "count" in body