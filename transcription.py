from openai import OpenAI
import os
from dotenv import load_dotenv
load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
def transcribe_audio(audio_file):
    """Transcribe audio using Whisper API."""
    try:
        transcription = client.audio.transcriptions.create(
            model="gpt-4o-transcribe", 
            file=audio_file
        )
        return transcription.text
    except Exception as e:
        raise Exception(f"Error during transcription: {str(e)}")
