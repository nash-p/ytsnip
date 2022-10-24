from unittest.loader import VALID_MODULE_NAME
from yt_dlp import YoutubeDL as ydl
import ffmpeg
import sys, getopt


test_url = "https://youtu.be/FtutLA63Cp8"  # Bad Apple, because yes
test_start = 6
test_end = 36


def get_secs(time_str) -> int:  # hehe

    h = "0"
    m = "0"
    s = "0"

    time_hms = time_str.split(":")

    if len(time_hms) == 1:
        s = time_hms[0]
    elif len(time_hms) == 2:
        m, s = time_hms
    elif len(time_hms) == 3:
        h, m, s = time_hms

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


def mince():
    pass


def main(argv):
    usage_str = "main.py -u <url> -o <outputfile> -s <starttime> -t <stoptime>"
    target_url = ""
    out_filename = ""
    start_time = "0"
    stop_time = ""

    try:
        opts, args = getopt.getopt(
            argv, "hu:o:s:t:", ["url=", "ofile=", "start=", "terminate="]
        )

    except getopt.GetoptError:
        print(usage_str)
        sys.exit(2)

    for opt, arg in opts:
        if opt == "-h":
            print(usage_str)
            sys.exit()
        elif opt in ("-u", "--url"):
            target_url = arg
        elif opt in ("-o", "--ofile"):
            out_filename = arg
        elif opt in ("-s", "--start"):
            start_time = arg
        elif opt in ("-t", "--terminate"):
            stop_time = arg

    stream_url, title = get_url(target_url)
    if out_filename != "":
        title = out_filename
    start_time = get_secs(start_time)
    stop_time = get_secs(stop_time)
    snip_url(stream_url, title, start_time, stop_time)


if __name__ == "__main__":
    main(sys.argv[1:])
