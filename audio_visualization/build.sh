#!/bin/sh

cd $(readlink -f "$(dirname "$0")")

mkdir build dist
ffmpeg -i "audio/in.flac" "build/in.wav"
python3 -m src.wave