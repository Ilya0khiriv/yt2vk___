import os
import subprocess
import time

import requests
from selenium.webdriver.support import expected_conditions as EC


from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
def p(text):
    d = __file__.split("/")[-1]
    print(f"[{d}] {text}")

def split_audio_and_video(input_video, output_audio, output_video):
    # Extract audio
    subprocess.run([
        'ffmpeg', '-i', input_video, '-q:a', '0', '-map', 'a', '-loglevel', 'quiet', output_audio
    ], check=True)

    # Extract video without audio
    subprocess.run([
        'ffmpeg', '-i', input_video, '-an', '-vcodec', 'copy', '-loglevel', 'quiet', output_video
    ], check=True)


# Example usage


def remove_voice(name, output_audio, no_vocal_audio):
    command = [
        './venv_new/bin/python3', './vocal-remover/inference.py',
        '--input', output_audio,
        '--tta',
        '--gpu', '0',
        '--output_dir', './videos'
    ]


    hh = subprocess.run(command, capture_output=True, text=True)
    print(hh)
    time.sleep(1)
    os.rename(f'./videos/{name}_split_Instruments.wav', no_vocal_audio)
    os.remove(f'./videos/{name}_split_Vocals.wav')




def merge_audio_video(video_path, audio_path, output_path):
    # FFmpeg command
    command = [
        'ffmpeg',
        '-i', video_path,
        '-i', audio_path,
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-strict', 'experimental',
        output_path
    ]

    # Run the FFmpeg command
    with open(os.devnull, 'w') as devnull:
        subprocess.run(command, stdout=devnull, stderr=subprocess.STDOUT)



name = "111"


def do_it(name, driver, downloader):
    input_video = f"{os.path.dirname(os.path.abspath(__file__))}/videos/{name}.mp4"
    output_audio = f"{os.path.dirname(os.path.abspath(__file__))}/videos/{name}_split.mp3"
    output_video = f"{os.path.dirname(os.path.abspath(__file__))}/videos/{name}_split.mp4"
    no_vocal_audio = f"{os.path.dirname(os.path.abspath(__file__))}/videos/{name}_no_vocal.mp3"

    split_audio_and_video(input_video, output_audio, output_video)
    remove_voice(name, output_audio, no_vocal_audio)
    os.remove(input_video)
    merge_audio_video(output_video, no_vocal_audio, input_video)
    os.remove(output_audio)
    os.remove(output_video)
    os.remove(no_vocal_audio)
    return
