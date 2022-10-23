lol
lmao
rip bozo

what I want to do:
1. Grab the funny stream url URL
yt-dlp -g "https://youtube.com/watch?fakeurl" 
    a. extract video url info dict
    b. grab format dict of first format with audio xtract that IS NOT None

2. Pass its output to ffmpeg
ffmpeg -ss 00:00:15.00 -i "OUTPUT-OF-FIRST URL" -t 00:00:10.00 -c copy out.mp4

where 00:00:00.00 is format HH:MM:SS.ms

simple
