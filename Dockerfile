FROM python:3.9

RUN useradd randomThought

WORKDIR /home/randomThought

ENV CRYPTOGRAPHY_DONT_BUILD_RUST=1

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN apt update
RUN apt install cmake
RUN venv/bin/pip install --upgrade pip setuptools wheel
RUN venv/bin/pip install -r requirements.txt
#Cryptography <3.5 is needed in order to not depend on having Rust
RUN venv/bin/pip install gunicorn pymysql cryptography==3.4

COPY app app
COPY migrations migrations
COPY randomThought.py config.py boot.sh ./
RUN chmod +x boot.sh

ENV FLASK_APP randomThought.py

RUN chown -R randomThought:randomThought ./
USER randomThought

EXPOSE 5000
ENTRYPOINT [ "./boot.sh" ]