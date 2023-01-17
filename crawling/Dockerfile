#셀레니움용 base image
FROM seleniarm/standalone-chromium:4
#user를 root로 지정해주지 않으면 apt-get으로 install 실패   
USER root 

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update
RUN apt-get install python3 -y
RUN apt install python3-pip -y
RUN apt-get install xvfb -y

WORKDIR /crawling
COPY requirements.txt fruits_crawling.py pymongo_tut.py Dockerfile ./
RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt
COPY . .


# https://stackoverflow.com/questions/69784773/headless-chrome-on-docker-m1-error-unable-to-discover-open-window-in-chrome
# https://hub.docker.com/layers/seleniarm/standalone-chromium/4/images/sha256-ce5e889d818a73b92a45f857ee9ae2b6b3b982cc981ad6d588b51d05327f1743?context=explore
