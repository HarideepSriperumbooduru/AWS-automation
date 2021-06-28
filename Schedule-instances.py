import json
import boto3
s3 = boto3.client('s3')

event_client = boto3.client('events')
lambda_client = boto3.client('lambda')
def lambda_handler(event, context):
    # TODO implement
    bucket = 'scraping123'
    key = 'schedule.json'
    response_s3 = s3.get_object(Bucket=bucket, Key= key)
    content = response_s3['Body']
    jsonObject = json.loads(content.read())
    scheduledTasks = jsonObject['tasks']
    for task in scheduledTasks:
        cronExp = task['CronExpression']
        instanceList = task['InstancesList']
        operation = task['Operation']
        eventName = task['EventRoleName']
    
        role_response = event_client.put_rule(
                                    Name=eventName,
                                    ScheduleExpression=cronExp,
                                    State='ENABLED'
                                )
        response = event_client.put_targets(
                                    Rule='Scheduling_Event',
                                    Targets=[
                                        {
                                            'Arn': 'arn:aws:lambda:ap-south-1:889667141700:function:Manage_EC2_Instance',
                                            'Id': '12345',
                                            'Input':json.dumps({"InstanceName":instanceList, "Operation":operation})
                                        }
                                    ]
                                )
        response = lambda_client.add_permission(
                                            FunctionName='arn:aws:lambda:ap-south-1:889667141700:function:Manage_EC2_Instance',
                                            StatementId='1425',
                                            Action='lambda:InvokeFunction',
                                            Principal='events.amazonaws.com',
                                            SourceArn=role_response['RuleArn']
                                        )
        print(response)
        return {
            'statusCode': 200,
            'body': json.dumps('Hello from Lambda!')
        }