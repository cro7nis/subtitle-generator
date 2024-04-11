import streamlit as st
import requests
import os
from PIL import Image
from loguru import logger
import time
from ui.configs import settings


def subtitle_request(url, task, fmt):
    response = requests.post(f'http://{settings.api.host}:{settings.api.port}/subtitle/api/v1/transcribe',
                             json={"url": url,
                                   "language": None,
                                   "outputDir": "outputs/",
                                   "task": task,
                                   "format": fmt},
                             )
    return response


def generate_subs(path, task, fmt):
    with st.spinner(text='Generating subtitles...'):
        response = subtitle_request(path, task.lower(), fmt)
        if response.status_code == 200:
            with open('file.' + fmt, 'wb') as s:
                s.write(response.content)
        else:
            logger.error(response.json())
            raise Exception('Something went wrong')

    return 'file.' + fmt


st.set_page_config(page_title="Subtitle generator", page_icon=":movie_camera:", layout="wide")
st.write("# Subtitle generator with faster whisper")

img = Image.open('assets/akash.png')
st.image(img, width=200)
st.markdown(
    "###### Made with :heart: by [@cro7nis](https://twitter.com/cro7nis)",
    unsafe_allow_html=True)

st.write(
    "The code is open source and available "
    "[here](https://github.com/cro7nis/subtitle-generator.git) on GitHub. "
    "Special thanks to the [faster whisper library](https://github.com/SYSTRAN/faster-whisper) :grin:"
)
# st.sidebar.write("## Upload and download :gear:")

st.write(
    "Input a YouTube link to generate subtitles.")

link = st.text_input("YouTube Link (The longer the video, the longer the processing time)")

task = st.selectbox("Select task. If you want to translate the subtibles to English language, select Translate.",
                    ["Transcribe", "Translate"], index=0)

fmt = st.selectbox("Select subtitle format.", ["srt", "vtt", "txt", "json", "tsv"], index=0)

subs_file = None
srt_file = None
txt_file = None
button = st.button("Get Subtitles")
if button:
    if link:
        try:
            subs_file = generate_subs(link, task, fmt)
        except Exception as e:
            logger.error(e)
            st.error("Something went wrong. Please try again")
    else:
        st.error("Please insert a youtube link")

    if subs_file:
        with st.spinner(text='Saving subtitles...'):
            time.sleep(1)
            with open(os.path.join(os.getcwd(), subs_file), "rb") as f:
                subtitles = f.read()

        dl_buttun = st.download_button(label=f"Download Subtibles (.{fmt})",
                                       data=subtitles,
                                       file_name=f"subtitles.{fmt}")
