from dotenv import load_dotenv

# Load environment variables from the "env.env" file in the current directory
load_dotenv("env.env")

# Access your environment variables
import os
aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY')
