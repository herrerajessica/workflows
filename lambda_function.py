import json
import boto3
import os
dynamodb = boto3.resource('dynamodb', region_name=os.getenv('AWS_REGION', 'us-east-1'))

table = dynamodb.Table('VisitorCounterTable')  # Nombre de la tabla actualizado

def lambda_handler(event, context):
    try:
        # Manejar la solicitud OPTIONS (Preflight CORS)
        if event.get("httpMethod") == "OPTIONS":
            return {
                "statusCode": 200,
                "headers": {
                    "Access-Control-Allow-Origin": "*",  # Permitir solicitudes desde cualquier origen
                    "Access-Control-Allow-Methods": "GET, OPTIONS",  # Métodos permitidos
                    "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Requested-With"  # Encabezados permitidos
                },
                "body": json.dumps("CORS preflight successful")
            }

        # Obtener el contador de visitas de DynamoDB
        response = table.get_item(Key={"ID": "counter"})  # Usamos el campo 'ID' en lugar de 'id'
        
        # Si no existe el campo 'counter', inicializamos el contador
        visits = 0
        if 'Item' in response:  # Esta línea está correctamente indentada
            visits = int(response["Item"].get("visits", 0)) + 1  # Esta línea también debe estar indentada
        else:
            # Si no existe el item, lo creamos con 1
            visits = 1  # Asegúrate de que esto esté indentado

        # Imprimir la respuesta de DynamoDB para depuración
        print("DynamoDB response:", response)  # Esta línea ahora está correctamente indentada

        # Actualizar el contador en DynamoDB
        table.put_item(Item={"ID": "counter", "visits": visits})

        # Responder con el número actualizado de visitas
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": "*",  # Permitir solicitudes desde cualquier origen
                "Access-Control-Allow-Methods": "GET, OPTIONS",  # Métodos permitidos
                "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Requested-With"  # Encabezados permitidos
            },
            "body": json.dumps({"visits": visits})  # Devolver las visitas
        }

    except Exception as e:
        # En caso de error, devolver un mensaje de error
        return {
            "statusCode": 500,
            "headers": {
                "Access-Control-Allow-Origin": "*",  # Permitir solicitudes desde cualquier origen
                "Access-Control-Allow-Methods": "GET, OPTIONS",  # Métodos permitidos
                "Access-Control-Allow-Headers": "Content-Type, Authorization, X-Requested-With"  # Encabezados permitidos
            },
            "body": json.dumps({"error": str(e)})  # Mensaje de error
        }
