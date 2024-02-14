set -ex

export IMAGEIO_FFMPEG_EXE=./ffmpeg

# python voiceover.py && python transcript.py && python visuals.py && python video.py && open video.mp4

# python voiceover.py
python transcript.py
python visuals.py
python video.py
open video.mp4
