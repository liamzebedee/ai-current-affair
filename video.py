from moviepy.editor import *
import os
from glob import glob
import random

import PIL



# Voiceover
audio = AudioFileClip("output.mp3")
audio.set_start(0)

# turn up 2x volume on the audio
audio = audio.volumex(13.4) # 2x volume, elevenlabs is quietttt

print(f"Audio duration: {audio.duration}")



all_clips = []
current_time = 0

frame_idx = 0

import json

# read the img_blocks.json file and parse json
blocks = json.load(open("img_blocks.json", "r"))

# for each block, create an image clip and a text clip
for block in blocks:
    start = block["start"]
    end = block["end"]
    dur = end - start

    # get the image path
    image_paths = block["image_paths"]

    img_length = dur / len(image_paths)
    print(f"img_length: {img_length}")
    for i, image_path in enumerate(image_paths):
        clip_start = start + i*img_length
        clip_end = start + (i+1)*img_length
        print("img_clip: " + image_path + f" {clip_start} {clip_end}")
        image_clip = ImageClip(image_path)
        image_clip = image_clip.resize((1920, 1080))
        image_clip = image_clip.set_start(clip_start).set_end(start + (i+1)*img_length)
        
        all_clips.append(image_clip)
    

    # create the image clip
    # image_clip = ImageClip(image_path)
    # image_clip.set_duration(image_duration)

    # if 1st frame, then the image covers full width height no matter what
    # image_clip = image_clip.resize((1920, 1080))
    # if frame_idx == 0:
    #     image_clip = image_clip.resize((1920, 1080))
    # else:
    #     # each image is a random size between 1/2 and 3/4 of the video
    #     image_clip = image_clip.resize((random.randint(1920 // 2, 1920 // 4 * 3), random.randint(1080 // 2, 1080 // 4 * 3)))

    text_clip = TextClip(
        block["image_query"], 
        fontsize=91, 
        # font is comic sans
        font="Comic-Sans-MS",
        bg_color='white',
        color='black'
    ).set_pos('center')
    text_clip = text_clip.set_start(block["start"]).set_end(block["end"])
    # all_clips.append(text_clip)

    # increment the current time
    current_time = block["end"]
    frame_idx += 1


import json
# now independently load the subtitles in using the data from the transcript
with open("transcript.json", "r") as f:
    transcript = json.load(f)
    
    # we want a subtitle every 10 words or so
    # so like convert words into subtitle chunks wiht their start and end index
    # then make a text clip for each chunk
    subtitle_chunks = []
    current_chunk = []
    for word in transcript["words"]:
        current_chunk.append(word)
        if len(current_chunk) > 10:
            subtitle_chunks.append(current_chunk)
            current_chunk = []
    # append the last chunk if it's not empty
    subtitle_chunks.append(current_chunk) if current_chunk else None

    print(subtitle_chunks)

    transcript_i = 0
    transcript_text = transcript["text"]

    # now make the text clips
    for i, chunk in enumerate(subtitle_chunks):
        # get the start and end times of the chunk
        start_time = float(chunk[0]["start"])
        end_time = float(chunk[-1]["end"])

        # get the text of the chunk, including punctuation from the original transcript
        # accumulate characters into text_buf until all words have been "scanned"
        text_buf = ""
        for word in chunk:
            raw_word = word["word"]
            
            # get next index of word
            j = transcript_i + transcript_text[transcript_i:].index(raw_word) + len(raw_word)

            text_buf += transcript_text[transcript_i:j]

            # peek next char, if it is "." or "!" or "?" then add it to the text_buf
            if j < len(transcript_text) and transcript_text[j] in [".", ",", "!", "?"]:
                text_buf += transcript_text[j]
                j += 1

            print(text_buf)
            transcript_i = j
        
        print(f"sub: {text_buf}")

        # text = " ".join([word["word"] for word in chunk])

        # make the text clip
        START_TIME_PADDING = -0.5  # -1.5
        text_clip = TextClip(
            text_buf, 
            fontsize=56, 
            # font is some Arial
            font="Arial",
            bg_color='black',
            color='yellow'
        ).set_pos('bottom').set_start(start_time + START_TIME_PADDING).set_end(end_time + START_TIME_PADDING).margin(20, color=(0, 0, 0))

        # append the text clip
        all_clips.append(text_clip)

# Loop through all clips and dump a "timesheet" of the format
# <clip_type> <40 char description> <start_time> <end_time>
# to stdout
for clip in all_clips:
    print(f"{clip} {clip.start} {clip.end}")



# make composite video
video = CompositeVideoClip(all_clips)

# Set the audio of the composite clip as your voiceover
video = video.set_audio(CompositeAudioClip([audio]))
video = video.set_duration(audio.duration)

# Export the video
video.write_videofile("video.mp4", fps=1, audio_codec='aac', codec='libx264')
