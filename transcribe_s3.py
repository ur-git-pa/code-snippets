import time
import boto3
import urllib.parse
import requests

transcribe = boto3.client('transcribe')
s3 = boto3.client('s3')

bucket_name = "modular-solutions-recordings"
destination_bucket = "transcribed-calls-modularsolutions"  # Change this to your desired destination bucket





# List objects in the bucket
objects = s3.list_objects_v2(Bucket=bucket_name)

for obj in objects.get('Contents', []):
    file_key = obj['Key']
    
    # Check if the object is an MP4 file
    if file_key.endswith('.mp4'):
        job_name = f"TranscribeJob-{int(time.time())}"  # Using a timestamp as a job name
        job_uri = f"https://s3.amazonaws.com/{bucket_name}/{file_key}"
        
        transcribe.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={'MediaFileUri': job_uri},
            MediaFormat='mp4',
            LanguageCode='en-US',
            MediaSampleRateHertz=32000
        )

        print(f"Transcription job started for: {file_key}")

        # Wait for job completion (similar to your existing code)
        while True:
            status = transcribe.get_transcription_job(TranscriptionJobName=job_name)
            if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
                break
            print(f"Transcription for {file_key} not ready yet...")
            time.sleep(5)

            
        if status['TranscriptionJob']['TranscriptionJobStatus'] == 'COMPLETED':
            transcription = transcribe.get_transcription_job(TranscriptionJobName=job_name)
    
    # Extract the transcript content from the response
            transcript_content = transcription['TranscriptionJob']['Transcript']['TranscriptFileUri']
            response = requests.get(transcript_content)
            transcript_content = response.content
            destination_key=f"{file_key}.json"
            s3.put_object(Body=transcript_content, Bucket=destination_bucket, Key=destination_key)
            print("Transcript content uploaded to S3.")
