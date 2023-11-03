from __future__ import print_function
 
import json
import boto3
ssm = boto3.client('ssm', 'us-west-2',aws_access_key_id=aws_access_key_id,
                    aws_secret_access_key=aws_secret_access_key)
response = ssm.get_parameters(
        Names=['OPENAIKEY'],WithDecryption=True
    )


parameter=response['Parameters']
openaikey=parameter[0]['Value']
openai.api_key=openaikey
