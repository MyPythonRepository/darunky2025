FROM python:3.13-slim

RUN apt update
RUN python --version

RUN mkdir /my_folder

WORKDIR /my_folder

COPY ./hello_world_from_docker.py ./hello_world.py
COPY ./requirements.txt ./requirements.txt

RUN python -m pip install --upgrade pip & pip install -r requirements.txt

CMD ["python", "hello_world.py"]
