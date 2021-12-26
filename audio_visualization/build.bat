@echo off

cd /d %~dp0

mkdir dist build
ffmpeg -i audio\in.flac build\in.wav
python -m src.wave