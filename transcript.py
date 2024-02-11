from openai import OpenAI
import os

# set OPENAI_API_KEY environment variable

client = OpenAI()

audio_file = open("output.mp3", "rb")
transcript = client.audio.transcriptions.create(
  file=audio_file,
  model="whisper-1",
  response_format="verbose_json",
  timestamp_granularities=["word"]
)

print(transcript.words)

# write transcript to file as json
with open("transcript.json", "w") as f:
    f.write(transcript.json())
