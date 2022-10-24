from yt_dlp import YoutubeDL as ydl
import ffmpeg, sys, os, getopt


default_url = "https://youtu.be/FtutLA63Cp8"  # Bad Apple, because yes
default_start = "5"
default_end = "15"

cur_path = os.getcwd()
output_path = os.path.join(cur_path, "out")
if not (os.path.exists(output_path) or os.path.isdir(output_path)):
    os.mkdir(output_path)


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
    info = ydl(ydl_opts).extract_info(url, download=False)  # dict of lists
    # info = ydl.sanitize_info(info)

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

    input = ffmpeg.input(url, ss=(start), to=(end))
    audio = input.audio
    out = audio.output(audio, ("out/" + title))

    return ffmpeg.run(out)


def mince(audio_file, folder_name, mince_length):

    folder = os.path.join(cur_path, "out", "minced", folder_name)
    if not os.path.exists(folder):
        os.makedirs(folder)

    os.chdir(folder)

    instream = ffmpeg.input(audio_file)
    out = instream.output(
        "audio_%d.mp4", f="segment", segment_time=mince_length, reset_timestamps=1
    )
    return ffmpeg.run(out)


def main(argv):

    usage_str = (
        "main.py -u <url> [-o <outputfile> -s <starttime> -t <stoptime> -m [<length>]]"
    )

    target_url = ""
    out_filename = ""
    start_time = default_start
    stop_time = default_end
    mince_folder = ""
    mince_length = 0
    to_mince = False

    try:
        opts, args = getopt.getopt(
            argv, "hu:ostm", ["url=", "ofile=", "start=", "terminate=", "mince="]
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
        elif opt in ("-m", "--mince"):
            to_mince = True
            mince_length = arg

        if target_url == "":
            print(usage_str)
            sys.exit(2)

        # URLs may have seperators
        target_url = target_url.rsplit("?")[0]

    stream_url, title = get_url(target_url)

    if out_filename != "":
        title = out_filename

    if mince_length == "":
        mince_length = 1

    mince_folder = title.rsplit(".")[0]

    start_time = get_secs(start_time)
    stop_time = get_secs(stop_time)

    snip_url(stream_url, title, start_time, stop_time)
    if to_mince:
        mince("../../" + title, mince_folder, mince_length)


if __name__ == "__main__":

    main(sys.argv[1:])
