from dotenv import load_dotenv

# Load environment variables from the "env.env" file in the current directory
load_dotenv("env.env")

# Access your environment variables
import os
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')


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
