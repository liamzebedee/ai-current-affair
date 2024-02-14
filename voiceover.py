import requests
import os

ELEVEN_API_KEY = os.environ.get("ELEVEN_API_KEY")
VOICE_AUSSIE = "nYz8PA65uq1aSPFXs0Ji"

CHUNK_SIZE = 1024
url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_AUSSIE}"

headers = {
  "Accept": "audio/mpeg",
  "Content-Type": "application/json",
  "xi-api-key": ELEVEN_API_KEY
}

data = {
  "text": open("text", "r").read(),
  "model_id": "eleven_multilingual_v2",
  "voice_settings": {
    "stability": 0.32,
    "similarity_boost": 0.54,
    "style": 0.94,
    "use_speaker_boost": True
    # "stability": 0.6,
    # "similarity_boost": 0.99,
    # "style": 0.64,
    # "use_speaker_boost": True
  }
}

response = requests.post(url, json=data, headers=headers)
# print response output
if response.status_code != 200:
    print(f"Error: {response.status_code}")
    print(response.text)
    exit(1)

with open('output.mp3', 'wb') as f:
    for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
        if chunk:
            f.write(chunk)
