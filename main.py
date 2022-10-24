from yt_dlp import YoutubeDL as ydl
import ffmpeg
import sys


test_url = "https://youtu.be/FtutLA63Cp8"  # Bad Apple, because yes
test_start = 6
test_end = 36


def get_secs(time_str) -> int:  # hehe
    h, m, s = time_str.split(":")
    secs = (int(h) * 3600) + (int(m) * 60) + int(s)
    return secs


# Extract Url
def get_url(url):

    ydl_opts = {}
    raw = ydl(ydl_opts).extract_info(url, download=False)  # dict of lists
    info = ydl.sanitize_info(raw)

    title = info["title"].strip() + ".mp4"

    formats = info["formats"]  # list of dicts
    audio_direct_url = ""
    for format in formats:
        if format["audio_ext"] != "none":
            audio_direct_url = format["url"]
            break

    # return r["formats"][-1]["url"]
    return audio_direct_url, title


def snip_url(url, title, start, end):
    input = ffmpeg.input(url)
    audio = input.audio
    # stream = ffmpeg.trim(audio, 60)
    out = ffmpeg.output(audio, ("out/" + title), ss=start, to=end)
    return ffmpeg.run(out)


if __name__ != "__main__":
    stream_url, title = get_url(test_url)
    snip_url(stream_url, title, test_start, test_end)


if __name__ == "__main__":
    print("LOG: Running main")
    args = sys.argv

    if len(args) < 4:
        print("ERROR: Not enough arguments")

    else:
        self_arg, target_url, start_time, end_time = args
        start_time = get_secs(start_time)
        end_time = get_secs(end_time)
        stream_url, title = get_url(target_url)
        snip_url(stream_url, title, start_time, end_time)
