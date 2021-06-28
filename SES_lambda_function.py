import json
import boto3
from botocore.exceptions import ClientError
client = boto3.client('ses')
def lambda_handler(event, context):
    # TODO implement
    SENDER = "pulugujja.shivan@msitprogram.net"
    RECIPIENTS = event['queryStringParameters']['RECIPIENTS']
    if not RECIPIENTS :
        return {
            'statusCode': 400,
            'body': json.dumps("Missing RECIPIENTS which is a required parameter")
        }
    CCADDRESSES = event['queryStringParameters']['CCADDRESSES']
    WEBSITE_NAME = event['queryStringParameters']['WEBSITE_NAME']
    SUBJECT = "Re: Scraping status of {} Spider".format(WEBSITE_NAME)
    IS_ERROR = event['queryStringParameters']['IS_ERROR']
    MESSAGE = event['queryStringParameters']['MESSAGE']
    WEBSITE_URL = event['queryStringParameters']['WEBSITE_URL']
    BODY_TEXT = ""
    if IS_ERROR :
        BODY_TEXT += "An error occured while scraping {} website \r\n".format(WEBSITE_NAME)
        BODY_TEXT += "Error "
    BODY_TEXT += "Message : \r\n"
    BODY_TEXT += "{} \r\n".format(MESSAGE)
    BODY_TEXT += "Website URL : {}".format(WEBSITE_URL)
    if IS_ERROR :
        BODY_HTML = """<html>
                            <head></head>
                            <body>
                                <p> An error occured while scraping {} website \r\n</p>
                                <h2>Error Message</h2>
                                <p>{}</p>
                                <p><a href='{}'><b>Website URL</b></a></p>
                            </body>
                        </html>
                    """.format(WEBSITE_NAME, MESSAGE, WEBSITE_URL)
    else :
        BODY_HTML = """<html>
                            <head></head>
                            <body>
                                <h2>Message</h2>
                                <p>{}</p>
                                <p><a href='{}'><b>Website URL</b></a></p>
                            </body>
                        </html>
                    """.format(MESSAGE, WEBSITE_URL)
    CHARSET = "UTF-8"
    try:
        response = client.send_email(
            Source=SENDER,
            Destination={
                'ToAddresses': RECIPIENTS,
                'CcAddresses': CCADDRESSES,
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
        return {
            'statusCode': 501,
            'body': json.dumps(e.response['Error']['Message'])
        }
    return {
        'statusCode': 200,
        'body': json.dumps(BODY_TEXT)
    }