import json
import boto3
import os

# Especificar la región explícitamente
region = os.getenv('AWS_REGION', 'us-east-1')
dynamodb = boto3.resource('dynamodb', region_name=region)
table = dynamodb.Table('VisitorCounterTable')

def lambda_handler(event, context):
    try:
        response = table.update_item(
            Key={'id': 'visitor_count'},
            UpdateExpression='ADD visits :inc',
            ExpressionAttributeValues={':inc': 1},
            ReturnValues='UPDATED_NEW'
        )
        return {
            "statusCode": 200,
            "body": json.dumps({"message": "Visit updated", "count": response["Attributes"]["visits"]})
        }
    
    except Exception as e:
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})  # Capturar el error para verlo en los logs
        }
