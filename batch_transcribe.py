import os
import openai
from dotenv import load_dotenv

load_dotenv("Credentials.env")

# Set your OpenAI API key
openai.api_key = os.getenv('OPEN_AI_KEY')

def batch_transcribe(input_folder, output_folder, model="whisper-1"):
    # Ensure output folder exists, create it if it doesn't
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Loop through files in the input folder
    for filename in os.listdir(input_folder):
        # Check if the file is a webm audio file (you can modify this condition based on your file types)
        if filename.endswith(".webm"):
            input_file_path = os.path.join(input_folder, filename)
            output_file_name = f"{os.path.splitext(filename)[0]}_transcript.txt"
            output_file_path = os.path.join(output_folder, output_file_name)
            
            # Read the audio file
            with open(input_file_path, "rb") as audio_file:
                # Create transcription
                transcript = openai.audio.transcriptions.create(
                    model=model,
                    file=audio_file
                )
                
                # Write transcript to output file
                with open(output_file_path, "w") as output_file:
                    output_file.write(transcript.text)
                    print(f"Transcription for {filename} saved to {output_file_path}")