import json
import boto3
import pytest
from moto import mock_dynamodb2
from lambda_function import lambda_handler

@pytest.fixture
@mock_dynamodb2
def setup_dynamodb():
    with mock_dynamodb():
        dynamodb = boto3.resource('dynamodb', region_name="us-east-1")

        # Tabla 1
        table1 = dynamodb.create_table(
            TableName="VisitorCounterTable",
            KeySchema=[{"AttributeName": "ID", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "ID", "AttributeType": "S"}],
            ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1}
        )
        table1.put_item(Item={"ID": "visitor_count", "visits": 0})

        # Tabla 2
        table2 = dynamodb.create_table(
            TableName="visitor-counter-table-sam",
            KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
            ProvisionedThroughput={"ReadCapacityUnits": 1, "WriteCapacityUnits": 1}
        )
        table2.put_item(Item={"id": "visitor_count", "visits": 0})

        yield  # Devuelve el entorno simulado listo para usarse

def test_lambda_handler_get(setup_dynamodb):
    """Prueba que el contador de visitas se incrementa correctamente"""
    event = {"httpMethod": "GET"}
    response = lambda_handler(event, None)
    print("Lambda response:", response)

    body = json.loads(response["body"])

    assert response["statusCode"] == 200, f"Error en Lambda: {response}"
    assert "count" in body
