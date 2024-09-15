import os
import subprocess

def layer_audio(video_file, audio_file, output_file):
    # FFmpeg command to layer audio on top of the original audio track
    command = [
        'ffmpeg',
        '-i', video_file,  # Input video file
        '-i', audio_file,  # Input audio file to layer
        '-filter_complex', '[0:a]volume=1.0[a0];[1:a]volume=1.0[a1];[a0][a1]amix=inputs=2:duration=first',
        # Mix audio tracks with specified volumes
        '-c:v', 'copy',  # Copy video codec
        '-loglevel', 'quiet',
        output_file  # Output file
    ]

    # Run the FFmpeg command
    with open(os.devnull, 'w') as devnull:
        subprocess.run(command, stdout=devnull, stderr=subprocess.STDOUT)



