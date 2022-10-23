from yt_dlp import YoutubeDL as ydl
import ffmpeg


test_url = "https://youtu.be/FtutLA63Cp8"  # Bad Apple, because yes
test_start_timestamp = 6
test_end_timestamp = 36

# Extract Url
def get_url(url) -> str:

    ydl_opts = {}
    raw = ydl(ydl_opts).extract_info(url, download=False)  # dict of lists
    info = ydl.sanitize_info(raw)

    formats = info["formats"]  # list of dicts
    audio_direct_url = ""
    for format in formats:
        if format["audio_ext"] != "none":
            audio_direct_url = format["url"]
            break

    # return r["formats"][-1]["url"]
    return audio_direct_url


def snip_url(url):
    input = ffmpeg.input(url)
    audio = input.audio
    # stream = ffmpeg.trim(audio, 60)
    out = ffmpeg.output(
        audio, "out.mp4", ss=test_start_timestamp, to=test_end_timestamp
    )
    return ffmpeg.run(out)


if __name__ == "__main__":
    print("LOG: Running main")
    stream_url = get_url(test_url)
    snip_url(stream_url)
