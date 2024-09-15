import os
import subprocess
import time

from json_to_srt import worker as json_to_srt


def act(id, path_folder, true_name):
    name = "lolka"

    try:
        os.remove(f"{path_folder}/{name}.srt")
        os.remove(f"{path_folder}/{name}.json")
        os.remove(f"{path_folder}/{name}.mp3")
    except:
        pass

    def cleanup():
        os.rename(f"{path_folder}/{name}.srt", f"{path_folder}/{true_name}.srt")
        os.rename(f"{path_folder}/{name}.mp3", f"{path_folder}/{true_name}.mp3")

    def do(command):
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            print("Output:", result.stdout)
        except subprocess.CalledProcessError as e:
            print("Command failed with return code:", e.returncode)
            print("Error output:", e.stderr)

    def audio():
        command = [
            'vot-cli',
            f'--output={path_folder}',
            f'--output-file={name}',
            link
        ]

        do(command)
        file_path = 'path/to/your/file.txt'

        if os.path.exists(f"{path_folder}/{name}.mp3"):
            print(f"Found - > {path_folder}/{name}.mp3")
            return 0
        else:
            print(f"NOT FOUND - > {path_folder}/{name}.mp3")
            return 1



    def subs():
        command = [
            'vot-cli',
            '--subs',
            f'--output={path_folder}',
            f'--output-file={name}',
            f'--reslang=ru',
            link
        ]

        do(command)

        old_name = f"{path_folder}/{name}.json"
        new_name = f"{path_folder}/{name}.srt"
        if json_to_srt(old_name, new_name) == 1:
            return 1
        return 0

    link = f"https://www.youtube.com/watch?v={id}"

    try_ = 0
    while True:
        if audio() == subs() == 0:
            cleanup()
            return 0

        try_ += 1
        if try_ > 5:
            return 1

# print(act(id="5bTBC8ayfIw", path_folder="./videos", true_name="112"))
