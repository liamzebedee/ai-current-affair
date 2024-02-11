from moviepy.editor import *
import os
from glob import glob
import random

import PIL

# Directory containing your images
img_dir = "imgs/"

# Get a list of all PNG, JPG, and JPEG files in the directory
image_files = glob(os.path.join(img_dir, "*.*"))

# filter anything not png, jpg, jpeg
image_files = [f for f in image_files if f.endswith(".png") or f.endswith(".jpg") or f.endswith(".jpeg")]

# sort by date
image_files.sort(key=os.path.getmtime)

print(image_files)




# Voiceover
audio = AudioFileClip("output.mp3")
audio.set_start(0)
print(f"Audio duration: {audio.duration}")

image_duration = audio.duration / len(image_files)


# Image clips
# image_clips = []
# text_clips = []

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
    image_path = block["image_paths"][0]
    # TODO UPDATE image_path to image_paths

    # create the image clip
    image_clip = ImageClip(image_path)
    # image_clip.set_duration(image_duration)

    # if 1st frame, then the image covers full width height no matter what
    if frame_idx == 0:
        image_clip = image_clip.resize((1920, 1080))
    else:
        # each image is a random size between 1/2 and 3/4 of the video
        image_clip = image_clip.resize((random.randint(1920 // 2, 1920 // 4 * 3), random.randint(1080 // 2, 1080 // 4 * 3)))

    # text_clip = TextClip(
    #     block["image_query"], 
    #     fontsize=112, 
    #     # font is comic sans
    #     font="Comic-Sans-MS",
    #     bg_color='white',
    #     color='black'
    # ).set_pos('center').set_duration(image_duration)

    # set the start times
    
    image_clip = image_clip.set_start(block["start"]).set_end(block["end"])
    # text_clip = text_clip.set_start(block["start"]).set_end(block["end"])

    # append the clisp
    all_clips.append(image_clip)
    # all_clips.append(text_clip)

    # increment the current time
    current_time = block["end"]
    frame_idx += 1


# for file_path in image_files:
#     image_clip = ImageClip(file_path)
#     image_clip.set_duration(image_duration)

#     # if 1st frame, then the image covers full width height no matter what
#     if frame_idx == 0:
#         image_clip = image_clip.resize((1920, 1080))
#     else:
#         # each image is a random size between 1/2 and 3/4 of the video
#         image_clip = image_clip.resize((random.randint(1920 // 2, 1920 // 4 * 3), random.randint(1080 // 2, 1080 // 4 * 3)))


#     # the image filename is of the format {index}_{query}.{ext}
#     # we want to extract the query and use it as the subtitle
#     query = file_path.split("_")[1].split(".")[0]
#     print(f"{current_time // 1}: {query}")

#     text_clip = TextClip(
#         query, 
#         fontsize=112, 
#         # font is comic sans
#         font="Comic-Sans-MS",
#         bg_color='white',
#         color='black'
#     ).set_pos('center').set_duration(image_duration)

#     # set the start times
#     image_clip = image_clip.set_start(current_time)
#     text_clip = text_clip.set_start(current_time)

#     # append the clisp
#     all_clips.append(image_clip)
#     all_clips.append(text_clip)

#     # increment the current time
#     current_time += image_duration
#     frame_idx += 1

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

    # now make the text clips
    for i, chunk in enumerate(subtitle_chunks):
        # get the start and end times of the chunk
        start_time = float(chunk[0]["start"])
        end_time = float(chunk[-1]["end"])

        # get the text of the chunk
        text = " ".join([word["word"] for word in chunk])

        # make the text clip
        text_clip = TextClip(
            text, 
            fontsize=64, 
            # font is some Arial
            font="Arial",
            bg_color='black',
            color='yellow'
        ).set_pos('bottom').set_start(start_time - 1.5).set_end(end_time - 1.5)

        # append the text clip
        all_clips.append(text_clip)

# make composite video
video = CompositeVideoClip(all_clips)

# Set the audio of the composite clip as your voiceover
video = video.set_audio(CompositeAudioClip([audio]))
video = video.set_duration(audio.duration)

# Export the video
video.write_videofile("video.mp4", fps=1, audio_codec='aac', codec='libx264')
