from dotenv import load_dotenv
import os

# load the environment variables from the .env file
load_dotenv()

# get the value of the MY_VAR environment variable
aws_access_key = os.environ['AWS_ACCESS_KEY_ID']
aws_secret_key = os.environ['AWS_SECRET_ACCESS_KEY']
