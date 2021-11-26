@echo off

cd /d %~dp0

mkdir dist
@REM mkdir build
@REM cd build
@REM ffmpeg -i ..\download\in.mp4 -i ..\download\in.m4a -vcodec copy -acodec copy out1.mp4
@REM ffmpeg -i out1.mp4 -ss 0:0:0 -to 0:4:37 -vcodec libx264 -acodec copy out2.mp4
@REM ffmpeg -i out2.mp4 -filter_complex "subtitles='../src/in.ass'" "..\dist\out.mp4"
ffmpeg -i 'download\in.mp4' -i 'download\in.m4a' -ss 0:0:0 -to 0:4:37 -vcodec libx264 -acodec copy -filter_complex "subtitles='src/in.ass'" dist\out.mp4