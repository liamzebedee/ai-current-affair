import requests
import os

import random

ELEVEN_API_KEY = os.environ.get("ELEVEN_API_KEY")
VOICE_AUSSIE = "nYz8PA65uq1aSPFXs0Ji"

CHUNK_SIZE = 1024
url = f"https://api.elevenlabs.io/v1/text-to-speech/{VOICE_AUSSIE}"

headers = {
  "Accept": "audio/mpeg",
  "Content-Type": "application/json",
  "xi-api-key": ELEVEN_API_KEY
}


def generate_voice_snippet(line):
    text = line
    print(f"Generating voice snippet for: {text}")
    # generate a unique filename based on the first 5 words concat + a unique 5 byte code
    # only have a-z chars
    sanitized = "".join([c for c in text if c.isalpha()]).lower()
    filename = " ".join(sanitized.split(' ')[0:5]) + "_" + str(random.randint(10000, 99999))

    data = {
        "text": text,
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
    
    print("Done")

    with open(f'files/{filename}.mp3', 'wb') as f:
        for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)





text = """Crikey, mates, it's the Croc Hunter on the beat,
Spittin' bars like I'm wrangling a croc by its feet.
In the concrete jungle, I'm the wild's voice,
Droppin' rhymes, savin' critters, makin' noise.

Like DOOM with his mask, I've got my khaki suit,
Protectin' animals, from the land to the fruit.
Supervillains in the world, poachers on the chase,
I'm here to save the day, in this wild, wicked race.""".split("\n")

# strip each line so no empties and just lines of text
lines = [line.strip() for line in text if line.strip()]

from concurrent.futures import ProcessPoolExecutor


if __name__ == '__main__':
    executor = ProcessPoolExecutor(max_workers=4)
    inputs_2d = [
        (line,) for line in lines
    ]
    image_2d_results = executor.map(generate_voice_snippet, *zip(*inputs_2d))
    image_2d_results = list(image_2d_results)