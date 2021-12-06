import boto3, json

def publish_note(msg):
    client = boto3.client('sns', region_name='us-east-1',
                          aws_access_key_id='AKIA2QZOYBRAXTZADA27',
                          aws_secret_access_key='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'
                          )
    txt_msg = json.dumps(msg)

    client.publish(TopicArn="arn:aws:sns:us-east-1:882417290070:ebay_store_topic",
                   Message=txt_msg)