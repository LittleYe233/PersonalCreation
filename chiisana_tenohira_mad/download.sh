cd $(readlink -f "$(dirname "$0")")

mkdir download && cd download
youtube-dl --format 136 https://www.youtube.com/watch?v=R6xAQxgA1sQ -o in.mp4
youtube-dl --format 140 https://www.youtube.com/watch?v=R6xAQxgA1sQ -o in.m4a