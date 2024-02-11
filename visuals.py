from openai import OpenAI
import os

# set OPENAI_API_KEY environment variable

import requests
from bs4 import BeautifulSoup
from bing_images import bing
from concurrent.futures import ProcessPoolExecutor

def search_images(query, limit=15):
    urls = bing.fetch_image_urls(query, limit=limit, extra_query_params='&first=1')
    return urls


def get_image_queries_2():
    import json
    # now independently load the subtitles in using the data from the transcript
    with open("transcript.json", "r") as f:
        transcript = json.load(f)
        
        # Split transcript.text into blocks of 2 sentences each that are in total more than 10 words
        sentences = transcript["text"].split(".")
        sentence_blocks = []
        current_block = ""
        for sentence in sentences:
            current_block += sentence + "."
            if len(current_block.split(" ")) > 10:
                sentence_blocks.append(current_block)
                current_block = ""
        sentence_blocks.append(current_block) if current_block else None
        print(f"len: {len(sentence_blocks)}")
        for s in sentence_blocks:
            print("- " + s)

        # This is the word list
        # "words":[{"word":"Oi","start":0.0,"end":0.47999998927116394},{"word":"listen","start":0.5799999833106995,"end":0.7599999904632568},{"word":"up","start":0.7599999904632568,"end":1.1200000047683716},{"word":"mates","start":1.1200000047683716,"end":1.2999999523162842},{"word":"Sam","start":1.7000000476837158,"end":1.8200000524520874},{"word":"Altman","start":1.8200000524520874,"end":2.059999942779541},{"word":"from","start":2.059999942779541,"end":2.319999933242798},{"word":"OpenAI's","start":2.319999933242798,"end":3.0799999237060547},{"word":"gone","start":3.0799999237060547,"end":3.200000047683716},{"word":"off","start":3.
    

        # Now run through the word array in the transcript, and annotate each sentence block with a start and end time
        start = transcript["words"][0]["start"]
        word_buf = []
        rem_words = transcript["words"]

        annot_sentence_blocks = []

        for sentence_block in sentence_blocks:
            # build up a word buf from the rem_words until we have matched the sentence string using a fuzzy matching (just a-Z with spaces)
            
            # just get the a-z lowercase of the sentence block
            sentence_block = ''.join(e for e in sentence_block.lower() if e.isalnum() or e.isspace())
            print(f"sentence_block: {sentence_block}")

            # now run through the words in the transcript and build up a word buffer until we have a match
            found_match = False
            for i, word in enumerate(rem_words):
                words_txt = ' '.join(w["word"] for w in rem_words[:i])
                word_txt_norm = ''.join(e for e in words_txt.lower() if e.isalnum() or e.isspace())

                print(f"word_buf #{i}: {word_txt_norm}")
                
                if word_txt_norm.replace(' ', '') == sentence_block.replace(' ', ''):
                    print("match")

                    # get the start and end times of the word buffer
                    start_time = float(rem_words[0]["start"])
                    end_time = float(word["end"])

                    print(f"start: {start_time}, end: {end_time}")

                    # annotate the sentence block with the start and end times
                    sentence_block = {
                        "text": words_txt,
                        "start": start_time,
                        "end": end_time
                    }
                    
                    annot_sentence_blocks.append(sentence_block)

                    rem_words = rem_words[i:]
                    break
        
        # now finally we can use the annotated sentence blocks to get the image queries

        for block in annot_sentence_blocks:
            subject = block["text"]

            prompt = f"I want you to help me make a youtube video. The video should basically have an image every 1s or so to keep the viewer engaged. Please read this voiceover and then output a one-line search query for visuals, no formatting. Example: luxury boat.\n\nVoiceover: {subject}"

            # call chatgpt
            openai = OpenAI()

            completion = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ]
            )

            one_line_search_qs = completion.choices[0].message.content
            print(one_line_search_qs)

            block["image_query"] = one_line_search_qs
        
        # now download all images one by one and save them in imgs

        search_images("black swan")

        # executor = ProcessPoolExecutor(max_workers=8)
        # inputs_2d = [
        #     (block["image_query"], 3) for block in annot_sentence_blocks
        # ]
        # image_2d_results = executor.map(download_img, *zip(*inputs_2d))
        # image_2d_results = list(image_2d_results)

        # for i, block in enumerate(annot_sentence_blocks):
        #     block["image_paths"] = image_2d_results[i]

        for block in annot_sentence_blocks:
            fnames = download_img(block["image_query"], n=3)
            block["image_paths"] = fnames
        
        # dump this info to a json file
        with open("img_blocks.json", "w") as f:
            f.write(json.dumps(annot_sentence_blocks))
            




def get_image_queries(subject):
    prompt = f"I want you to help me make a youtube video. The video should basically have an image every 1s or so to keep the viewer engaged. Please read this voiceover and then output a list of one-line search queries for visuals, no formatting.\n\nVoiceover: {subject}"

    # call chatgpt
    openai = OpenAI()

    completion = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    one_line_search_qs = completion.choices[0].message.content
    print(one_line_search_qs)

    # parse them
    parsed_qs = []
    for line in one_line_search_qs.split("\n"):
        # strip "-", any ordered list numbers (e.g. "1. "), and any leading/trailing whitespace
        line = line.lstrip("-").lstrip("1234567890.").strip()
        # print(line)
        parsed_qs.append(line)
    
    print(parsed_qs)

    return parsed_qs

def download_img(query, n=3):
    urls = search_images(query)
    i = 0

    fnames = []

    while len(urls) > 0:
        url_candidate = urls.pop(0)

        try:
            print(f"img {i} url: {url_candidate}")
            img = requests.get(url_candidate)
        except:
            continue

        # check status code
        if img.status_code != 200:
            continue

        # detect ext
        ext = img.headers['Content-Type'].split("/")[1]
        print(ext)

        # save as {index}_{query} with the extension given in the response
        # shorten query to 24 chars
        query = query[:16]
        fname = f"imgs/{i}_{query}.{ext}"
        with open(fname, "wb") as f:
            f.write(img.content)
        
        fnames.append(fname)
        i += 1

        if i >= n:
            break

    return fnames

def download_images(parsed_qs):
    # search for images
    for query in parsed_qs:
        i = 0
        urls = search_images(query)
        
        while len(urls) > 0:
            url_candidate = urls.pop(0)

            img = requests.get(url_candidate)
            print(f"img {i} url: {url_candidate}")

            # check status code
            if img.status_code != 200:
                continue

            # detect ext
            ext = img.headers['Content-Type'].split("/")[1]
            print(ext)

            # save as {index}_{query} with the extension given in the response
            with open(f"imgs/{i}_{query}.{ext}", "wb") as f:
                f.write(img.content)
        
        i += 1




# get_image_queries("""Oi, listen up, mates! Sam Altman from OpenAI's gone off the deep end, reckon he's after a swag of cash bigger than a croc's appetite – we're talking trillions, not just a few shrimp on the barbie! This bloke's chattin' up investors left and right, even had a yarn with the bigwigs over in the United Arab Emirates. Picture this: he's dreaming of a tech bonanza that's gonna need a cheeky $7 trillion! You could buy a whole lot of snags and beers with that, I tell ya.

# So, what's this grand plan? Sammy wants to chuck up heaps of chip foundries faster than a kangaroo on a hot tin roof, and get the old hands at it, like Taiwan Semiconductor Manufacturing Company, to run the show. Why? 'Cause he's hit a snag with not enough chips to power his AI toys like ChatGPT. He reckons it's a bigger drought than the Nullarbor.

# And get this, he's not just spinning yarns at the pub. He's been hobnobbing with top dogs from TSMC, the U.S. Secretary of Commerce, and even SoftBank's big cheese. All while countries are scrambling like a mob of emus to pump out their own chips, but still, the big boys like TSMC and NVIDIA are holding the fort.

# OpenAI, backed by the mighty Microsoft, is keeping mum, but they've whispered they're keen as mustard to boost the global tech BBQ. And Sam Altman, he's the larrikin leading the charge, bouncing back from getting the boot like a true blue Aussie battler.

# So, to wrap it up: Sam's after a treasure chest so big it'd make Blackbeard blush, aiming to turn the AI world upside down. It's a wild ride, but if anyone can wrangle this croc, it's our mate Sam. Let's just hope he doesn't end up a few kangaroos loose in the top paddock!""")

get_image_queries_2()