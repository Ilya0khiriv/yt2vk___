import subprocess




def insert_subtitles(input_video, subtitles, output_video):
    command = [
        'ffmpeg',
        '-i', input_video,
        '-vf',
        f"subtitles={subtitles}:force_style='FontName=Arial,PrimaryColour=&HFFFFFF,BackColour=&H000000,BorderStyle=4,Outline=1,MarginV=40,FontSize=8'",
        '-c:a', 'copy',
        '-loglevel', 'quiet',
        output_video
    ]

    subprocess.run(command)


