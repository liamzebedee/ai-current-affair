ai a current affair
===================

An automatic low-value (shitpost) Aussie newsreel pipeline.

[Here's an example](https://www.youtube.com/watch?v=XWq1ZKU3GNo) newsreel about the Ethereum Virtual Machine, narrated by an Aussie cobba.

![](./screenshot.png)

 * news stories are ingested into chatgpt
 * then turned into a rick and morty script
 * then rewritten as an australian narrator
 * voiceover is generated using elevenlabs tuned with steve irwin clips
 * openai whisper is used to extract the transcript along with timings of certain words
 * this transcript is used to split the voiceover text into chunks, which we then analyse using chatgpt for visual content
 * bing image search is scraped and we get these visuals
 * the entire video is put together using moviepy and ffmpeg


## Pipeline

```
news stories -> aussie voiceover -> elevenlabs voice mp3 -> openai whisper transcript -> story visuals from chatgpt/bing -> video generated by ffmpeg
```

## Setup

 * `cp .env.example .env` add api keys
 * ffmpeg binary, set using `export IMAGEIO_FFMPEG_EXE=./ffmpeg`
 * imagemagick

## Run

```sh
./run.sh
```