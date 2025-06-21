FROM python:3.12-slim

RUN apt update & mkdir /darunky

WORKDIR /darunky

COPY ./src ./src
COPY ./commands ./commands
COPY ./requirements.txt ./requirements.txt

RUN python -m pip install --upgrade pip & pip install -r requirements.txt

#RUN chmod +x ./commands/start_server_dev.sh

CMD ["bash"]

#CMD ["python", "src/manage.py", "runserver", "0:8010"]
