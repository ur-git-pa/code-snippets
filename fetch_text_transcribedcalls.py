import boto3
import json

# Initialize S3 client
s3 = boto3.client('s3')

# Define your bucket and prefix
bucket_name = 'transcribed-calls-modularsolutions'

# List objects in the bucket with the specified prefix
response = s3.list_objects_v2(Bucket=bucket_name)

# Prefix for new .txt files
output_prefix = 'transcripts_'  # Prefix for the new .txt files

# Iterate through the objects
for index, obj in enumerate(response.get('Contents', [])):
    # Get the object key
    file_key = obj['Key']
    
    # Get the object from S3
    obj = s3.get_object(Bucket=bucket_name, Key=file_key)
    
    # Get the content (assuming it's in bytes)
    transcript_content = obj['Body'].read()
    
    # Decode the bytes string to a regular string and load it as JSON
    json_str = transcript_content.decode('utf-8')
    data = json.loads(json_str)
    
    # Extract the transcript text from the JSON data
    transcript = data['results']['transcripts'][0]['transcript']
    
    # Define the new file key for the transcript .txt file
    new_file_key = f'{output_prefix}{index + 1}.txt'  # e.g., output_folder/transcripts_1.txt
    
    # Upload the transcript text as a new .txt file to S3
    s3.put_object(Bucket=bucket_name, Key=new_file_key, Body=transcript.encode('utf-8'))

    print(f"Transcript {index + 1} uploaded as {new_file_key}")
