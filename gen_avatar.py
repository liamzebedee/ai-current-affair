files = [
    ("input_face", open("avatar.png", "rb")),
    ("input_audio", open("output.mp3", "rb"))
]

payload = {
    "face_padding_top": 3,
    "face_padding_bottom": 16,
    "face_padding_left": 12,
    "face_padding_right": 6,
    "text_prompt": "Oi, listen up, mates! Sam Altman from OpenAI's gone off the deep end, reckon he's after a swag of cash bigger than a croc's appetite – we're talking trillions, not just a few shrimp on the barbie! This bloke's chattin' up investors left and right, even had a yarn with the bigwigs over in the United Arab Emirates. Picture this: he's dreaming of a tech bonanza that's gonna need a cheeky $7 trillion! You could buy a whole lot of snags and beers with that, I tell ya.\n\nSo, what's this grand plan? Sammy wants to chuck up heaps of chip foundries faster than a kangaroo on a hot tin roof, and get the old hands at it, like Taiwan Semiconductor Manufacturing Company, to run the show. Why? 'Cause he's hit a snag with not enough chips to power his AI toys like ChatGPT. He reckons it's a bigger drought than the Nullarbor.\n\nAnd get this, he's not just spinning yarns at the pub. He's been hobnobbing with top dogs from TSMC, the U.S. Secretary of Commerce, and even SoftBank's big cheese. All while countries are scrambling like a mob of emus to pump out their own chips, but still, the big boys like TSMC and NVIDIA are holding the fort.\n\nOpenAI, backed by the mighty Microsoft, is keeping mum, but they've whispered they're keen as mustard to boost the global tech BBQ. And Sam Altman, he's the larrikin leading the charge, bouncing back from getting the boot like a true blue Aussie battler.\n\nSo, to wrap it up: Sam's after a treasure chest so big it'd make Blackbeard blush, aiming to turn the AI world upside down. It's a wild ride, but if anyone can wrangle this croc, it's our mate Sam. Let's just hope he doesn't end up a few kangaroos loose in the top paddock!",
    "tts_provider": "ELEVEN_LABS",
    "uberduck_voice_name": "the-rock",
    "uberduck_speaking_rate": 1,
    "google_voice_name": "en-GB-Neural2-D",
    "google_speaking_rate": 0.9,
    "google_pitch": -2.5,
    "bark_history_prompt": None,
    "elevenlabs_voice_name": None,
    "elevenlabs_api_key": None,
    "elevenlabs_voice_id": "y3hDSCFhlXYcFCo919yY",
    "elevenlabs_model": "eleven_multilingual_v2",
    "elevenlabs_stability": 0.8,
    "elevenlabs_similarity_boost": 0.75,
    "elevenlabs_style": 0,
    "elevenlabs_speaker_boost": True,
}



api_key = "sk-"

import requests
import json
try:
    response = requests.post(
        "https://api.gooey.ai/v2/LipsyncTTS/form/?run_id=67tane883d2k&uid=LCvoHCFOmCgJrzMJ0dtY3henqdF2",
        headers={
            "Authorization": "Bearer " + api_key,
        },
        files=files,
        data={"json": json.dumps(payload)},
    )
    response.raise_for_status()

    res = response.json()
    print(res)
except requests.exceptions.HTTPError as err:
    print(err)

