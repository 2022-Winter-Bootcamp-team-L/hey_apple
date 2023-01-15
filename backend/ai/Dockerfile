FROM python:3.8

WORKDIR /ai
COPY requirements.txt /ai

RUN apt update && apt install --no-install-recommends -y zip htop screen libgl1-mesa-glx build-essential

RUN pip install --upgrade pip
RUN pip install --no-cache -r requirements.txt
