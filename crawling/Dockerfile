# FROM ubuntu:20.04

# ENV PYTHONDONTWRITEBYTECODE 1
# ENV PYTHONUNBUFFERED 1

# WORKDIR /crawling

# RUN apt update -y
# RUN apt install python3.8 -y
# RUN apt install vim -y
# RUN apt install net-tools -y
# RUN apt install iputils-ping -y
# RUN apt install python3-pip -y

# RUN apt-get -y install wget
# RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
# RUN apt install ./google-chrome-stable_current_amd64.deb
# RUN apt-get update 
# RUN apt-get install google-chrome-stable 

# COPY requirements.txt ./
# RUN pip install --upgrade pip
# RUN pip install --no-cache-dir -r requirements.txt
# RUN echo 'alias python=python3.8' >> .bashrc

# COPY . /crawling







FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1



WORKDIR /crawling

RUN apt update && apt install --no-install-recommends -y zip htop screen libgl1-mesa-glx build-essential
RUN apt-get -y update
RUN apt install wget
RUN apt install unzip
RUN apt-get -y install xvfb
RUN wget -P /crawling https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt -y install ./google-chrome-stable_current_amd64.deb
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/` curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip -d /crawling


COPY requirements.txt ./
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . /crawling








