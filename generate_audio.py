import requests
import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# Set your API key
api_key = os.getenv("ELEVENLABS_API_KEY")
if not api_key:
    raise ValueError("ELEVENLABS_API_KEY not found in .env file")


def generate_audio(text_file_path, voice_id="21m00Tcm4TlvDq8ikWAM", speed=1.0):
    # Read text from file
    try:
        with open(text_file_path, "r", encoding="utf-8") as f:
            text = f.read().strip()
        if not text:
            raise ValueError("Text file is empty")
    except FileNotFoundError:
        print(f"❌ Error: Text file '{text_file_path}' not found")
        return
    except Exception as e:
        print(f"❌ Error reading text file: {str(e)}")
        return

    # Correct endpoint with voice_id in the URL
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

    headers = {
        "xi-api-key": api_key,  # ElevenLabs uses xi-api-key header
        "Content-Type": "application/json"
    }

    # Define the payload
    payload = {
        "text": text,
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.5,
            "style": 0.5,
            "use_speaker_boost": True,
            "speed": speed
        }
    }

    # Ensure output directory exists
    os.makedirs("output", exist_ok=True)

    # Send the request to generate the audio
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        output_filename = "output/output_audio.mp3"
        with open(output_filename, "wb") as f:
            f.write(response.content)
        print(f"✅ Audio saved successfully to {output_filename}")
    else:
        print(f"❌ Error: {response.status_code}")
        try:
            print("Error details:", response.json())
        except ValueError:
            print("Raw response:", response.text)


# Example usage
generate_audio("output/video_script.txt", voice_id="21m00Tcm4TlvDq8ikWAM", speed=1.0)