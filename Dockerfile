FROM jrottenberg/ffmpeg:4.0-alpine

RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y python3 python3-pip python3-dev
RUN python -m pip install --upgrade pip
