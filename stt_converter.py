import os
import requests
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs

# Load environment variables
load_dotenv()

def get_client():
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY not found in environment variables.")
    return ElevenLabs(api_key=api_key)

def download_audio(url, save_path="temp_audio.mp3"):
    """Downloads audio from a URL to a local file."""
    print(f"Downloading audio from {url}...")
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Audio saved to {save_path}")
        return save_path
    except Exception as e:
        print(f"Error downloading audio: {e}")
        return None

def transcribe_audio(file_path):
    """Transcribes the given audio file using ElevenLabs API."""
    client = get_client()
    
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    print(f"Transcribing {file_path}...")
    try:
        with open(file_path, "rb") as audio_file:
            response = client.speech_to_text.convert(
                model_id="scribe_v2",
                file=audio_file,
                language_code='en',
                tag_audio_events=False,
                num_speakers=1,
                timestamps_granularity='word',
                diarize=False,
            )
        return response
    except Exception as e:
        print(f"Error during transcription: {e}")
        return None

def main():
    print("ElevenLabs Speech-to-Text Converter")
    print("1. Local File")
    print("2. URL")
    
    choice = input("Enter your choice (1 or 2): ").strip()
    
    audio_file_path = None
    temp_file_created = False

    if choice == '1':
        audio_file_path = input("Enter the path to the audio file: ").strip()
        # Remove quotes if user dragged and dropped file
        if audio_file_path.startswith('"') and audio_file_path.endswith('"'):
            audio_file_path = audio_file_path[1:-1]
            
    elif choice == '2':
        url = input("Enter the URL of the audio file: ").strip()
        audio_file_path = download_audio(url)
        if audio_file_path:
            temp_file_created = True
    else:
        print("Invalid choice.")
        return

    if audio_file_path:
        result = transcribe_audio(audio_file_path)
        if result:
            print("\n--- Transcription Result ---")
            print(result.text)
            print("----------------------------")
        
        # Clean up temp file if we created it
        if temp_file_created and os.path.exists(audio_file_path):
            os.remove(audio_file_path)
            print(f"Temporary file {audio_file_path} removed.")

if __name__ == "__main__":
    main()
