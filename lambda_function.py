import json
import boto3
import os
from decimal import Decimal

def lambda_handler(event, context):
    try:
        # Inicializar DynamoDB dentro de la función
        region = os.getenv('AWS_REGION', 'us-east-1')
        dynamodb = boto3.resource('dynamodb', region_name=region)
        table = dynamodb.Table('VisitorCounterTable')

        response = table.update_item(
            Key={'ID': 'visitor_count'},
            UpdateExpression='ADD visits :inc',
            ExpressionAttributeValues={':inc': 1},
            ReturnValues='UPDATED_NEW'
        )

        # Convertir Decimal a int antes de serializar JSON
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Visit updated", "count": int(response["Attributes"]["visits"])})
        }
    
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})  # Capturar el error para verlo en los logs
        }
