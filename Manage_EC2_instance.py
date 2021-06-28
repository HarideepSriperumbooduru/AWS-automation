import json
import boto3
client = boto3.client('lightsail')
def lambda_handler(event, context):
    # TODO implement
    if event.get('Operation'):
        operation=event.get('Operation')
        if event.get('InstanceName'):
            instances = event['InstanceName']
            for instance in instances:
                if operation=='start':
                    response = client.start_instance(
                        instanceName=instance
                    )
                    return {
                        'statusCode': 200,
                        'body': json.dumps('Successfully Started the Instance!!!')
                    }
                elif operation=='stop':
                    response = client.stop_instance(
                        instanceName=instance,
                        force=True
                    )
                    return {
                        'statusCode': 200,
                        'body': json.dumps('Stopped the instance sucessfully!!!')
                    }
    return {
       'statusCode': 400,
        'body': json.dumps('Something went wrong')
    } 
