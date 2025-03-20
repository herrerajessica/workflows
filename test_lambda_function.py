import json
import boto3
import pytest
from moto import mock_aws
from lambda_function import lambda_handler  # Asegúrate de importar correctamente tu Lambda

TABLE_NAME = "VisitorCounterTable"

@pytest.fixture
def setup_dynamodb():
    """Mockea una tabla de DynamoDB con datos de prueba"""
    with mock_aws():  # Usamos mock_aws() en lugar de mock_dynamodb()
        dynamodb = boto3.resource("dynamodb", region_name="us-east-1")
        table = dynamodb.create_table(
            TableName=TABLE_NAME,
            KeySchema=[{"AttributeName": "ID", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "ID", "AttributeType": "S"}],
            BillingMode="PAY_PER_REQUEST",
        )
        table.put_item(Item={"ID": "counter", "visits": 5})
        yield table  # Devolver la tabla para su uso en las pruebas

def test_lambda_handler_get(setup_dynamodb):
    """Prueba que el contador de visitas se incrementa correctamente"""
    event = {"httpMethod": "GET"}
    response = lambda_handler(event, None)
    body = json.loads(response["body"])
    
    assert response["statusCode"] == 200
    assert "visits" in body
    assert body["visits"] == 6  # La visita debería haber aumentado de 5 a 6

