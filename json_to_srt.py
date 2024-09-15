import json
import os

def worker(old, new):
    try:
        with open(old, "r") as file:
            json_data = file.read()
    except:
        return 1

    # Parse JSON data
    data = json.loads(json_data)

    # Convert milliseconds to SRT timestamp format
    def ms_to_srt_time(ms):
        seconds, milliseconds = divmod(int(ms), 1000)
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

    # Split long lines into smaller chunks
    def split_lines(text, max_chars=42):
        words = text.split()
        lines = []
        current_line = []
        current_length = 0
        for word in words:
            if current_length + len(word) + (1 if current_line else 0) <= max_chars:
                current_line.append(word)
                current_length += len(word) + (1 if current_line else 0)
            else:
                lines.append(' '.join(current_line))
                current_line = [word]
                current_length = len(word)
        if current_line:
            lines.append(' '.join(current_line))
        return lines

    # Convert to SRT format
    srt_output = []
    subtitle_index = 1
    for subtitle in data['subtitles']:
        start_time = subtitle['startMs']
        end_time = subtitle['startMs'] + subtitle['durationMs']
        text_lines = split_lines(subtitle['text'])

        # Calculate duration per line based on the number of words
        total_words = sum(len(line.split()) for line in text_lines)
        if total_words == 0:
            continue
        duration_per_word = subtitle['durationMs'] / total_words

        for i, line in enumerate(text_lines):
            words_in_line = len(line.split())
            line_duration = words_in_line * duration_per_word
            line_start_time = ms_to_srt_time(start_time)
            line_end_time = ms_to_srt_time(start_time + line_duration)
            srt_output.append(f"{subtitle_index}")
            srt_output.append(f"{line_start_time} --> {line_end_time}")
            srt_output.append(line)
            srt_output.append("")  # Blank line after each subtitle
            subtitle_index += 1
            start_time += line_duration

    # Join all lines into the final SRT content
    srt_content = "\n".join(srt_output)

    with open(new, "w") as file:
        file.write(srt_content)
        os.remove(old)