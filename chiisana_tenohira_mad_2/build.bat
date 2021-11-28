@echo off

cd /d %~dp0

mkdir dist
ffmpeg -i 'download\in.flv' -ss 0:0:0 -to 0:4:41 -vcodec h264 -b:v 968K -time_base 1/1000 -enc_time_base 1/50 -r 25 -acodec copy -filter_complex "subtitles='src/in.ass'" dist\out.flv